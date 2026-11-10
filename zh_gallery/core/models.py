"""Модели галереи: категория → подкатегория → медиа-элемент + отзывы.

Ключевые изменения относительно исходной версии:

* slug генерируется один раз (раньше перезаписывался на каждом save() и ломал
  существующие ссылки), уникальность внутри «родителя» держится суффиксом;
* ``MediaItem.like_time`` — это время последнего лайка, а не время последнего
  save() (было ``auto_now=now()``, то есть обновлялось при любом сохранении);
* тайтлы больше не уникальны глобально: «Закат» может быть в двух подкатегориях;
* ``get_absolute_url`` собирается через reverse() и не падает на «сиротах»;
* удаление/замена картинки чистит файл через storage, а не через отдельный
  WebDAV-клиент внутри сигнала (работает и с локальным диском, и с Nextcloud).
"""

from __future__ import annotations

import logging
from pathlib import Path

from django.conf import settings
from django.db import models
from django.db.models import Count
from django.db.models.signals import post_delete, pre_save
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from slugify import slugify

logger = logging.getLogger(__name__)


class SluggedModel(models.Model):
    """Абстрактная база: человекочитаемый slug, который не меняется при правках."""

    slug = models.SlugField(_("slug"), max_length=255, blank=True, db_index=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.build_unique_slug()
        super().save(*args, **kwargs)

    def slug_source(self) -> str:
        """Строка, из которой строится slug."""
        return self.title

    def slug_siblings(self) -> models.QuerySet:
        """Набор объектов, среди которых slug должен быть уникальным."""
        raise NotImplementedError

    def build_unique_slug(self) -> str:
        base = slugify(self.slug_source()) or "item"
        candidate = base
        index = 2
        siblings = self.slug_siblings().exclude(pk=self.pk)
        while siblings.filter(slug=candidate).exists():
            candidate = f"{base}-{index}"
            index += 1
        return candidate


class MainCategory(SluggedModel):
    """Верхний уровень навигации: «Живопись», «Фотография» и т.п."""

    title = models.CharField(_("title"), max_length=255, unique=True)
    preview_item = models.ForeignKey(
        "MediaItem",
        verbose_name=_("Preview from media"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_("Leave empty to use the uploaded image"),
    )

    class Meta:
        verbose_name = _("main category")
        verbose_name_plural = _("main categories")
        ordering = ["title"]

    def __str__(self) -> str:
        return self.title

    def get_absolute_url(self) -> str:
        return reverse("category_view", args=[self.slug])

    @property
    def preview_image(self):
        """Превью: выбранная работа, иначе — загруженная картинка (если есть)."""
        if self.preview_item_id and self.preview_item.image:
            return self.preview_item.image
        return getattr(self, "image", None)

    def slug_siblings(self) -> models.QuerySet:
        return MainCategory.objects.all()


class SubCategory(SluggedModel):
    """Раздел внутри категории. Слаги уникальны внутри категории."""

    category = models.ForeignKey(
        MainCategory,
        verbose_name=_("category"),
        related_name="subcategories",
        on_delete=models.CASCADE,
        # null=True — наследие старых данных; в формах и админке поле обязательное
        null=True,
        blank=False,
    )
    title = models.CharField(_("title"), max_length=255)
    image = models.ImageField(_("image"), upload_to="subcategories/", null=True, blank=True)
    description = models.CharField(_("description"), max_length=255, blank=True, default="")
    preview_item = models.ForeignKey(
        "MediaItem",
        verbose_name=_("Preview from media"),
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        help_text=_("Leave empty to use the uploaded image"),
    )

    class Meta:
        verbose_name = _("subcategory")
        verbose_name_plural = _("subcategories")
        ordering = ["title"]

    def __str__(self) -> str:
        return f"{self.category}: {self.title}" if self.category_id else self.title

    def get_absolute_url(self) -> str:
        if not self.category_id:
            return reverse("frontpage_view")
        return reverse("subcategory_view", args=[self.category.slug, self.slug])

    @property
    def preview_image(self):
        """Превью: выбранная работа, иначе — загруженная картинка."""
        if self.preview_item_id and self.preview_item.image:
            return self.preview_item.image
        return self.image

    def slug_siblings(self) -> models.QuerySet:
        return SubCategory.objects.filter(category_id=self.category_id)


class MediaItemQuerySet(models.QuerySet):
    """Аннотации, которые убирают N+1 в шаблонах."""

    def with_stats(self) -> MediaItemQuerySet:
        return self.select_related("subcategory", "subcategory__category").annotate(
            likes_count=Count("likes", distinct=True),
            reviews_count=Count("reviews", distinct=True),
        )

    def liked_recently(self) -> MediaItemQuerySet:
        return self.filter(like_time__isnull=False).order_by("-like_time")


def media_item_upload_to(instance: MediaItem, filename: str) -> str:
    """Раскладываем работы по папкам подкатегорий: ``<slug подкатегории>/<имя>``.

    Раньше файлы уходили в ``media_items/<год>/<месяц>/`` — это неудобно при
    просмотре в Nextcloud. Теперь путь зависит от подкатегории, а имя файла
    транслитерируется, чтобы не было кириллицы и пробелов.
    """
    parts = ["bez-kategorii"]
    if instance.subcategory_id:
        subcategory = instance.subcategory
        category = subcategory.category
        parts = [category.slug or "bez-kategorii", subcategory.slug or "bez-kategorii"]

    stem = slugify(Path(filename).stem)[:60] or "image"
    suffix = Path(filename).suffix.lower() or ".jpg"
    return "/".join(parts) + f"/{stem}{suffix}"


class MediaItem(SluggedModel):
    """Картинка галереи; счётчик просмотров и лайки живут здесь же."""

    subcategory = models.ForeignKey(
        SubCategory,
        verbose_name=_("subcategory"),
        related_name="media_items",
        on_delete=models.CASCADE,
        null=True,
        blank=False,
    )
    title = models.CharField(_("title"), max_length=255)
    description = models.CharField(_("description"), max_length=255, blank=True, default="")
    description_generated_by_ai = models.BooleanField(
        _("description generated by AI"), default=False
    )
    image = models.ImageField(_("image"), upload_to=media_item_upload_to)

    views = models.PositiveIntegerField(_("views"), default=0, editable=False)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("likes"),
        related_name="liked_items",
        blank=True,
    )
    like_time = models.DateTimeField(
        _("last like time"), null=True, blank=True, editable=False, db_index=True
    )

    objects = MediaItemQuerySet.as_manager()

    class Meta:
        verbose_name = _("media item")
        verbose_name_plural = _("media items")
        ordering = ["title"]
        indexes = [
            models.Index(fields=["-like_time"], name="mediaitem_like_time_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.id}, {self.subcategory}: {self.title}"

    def get_absolute_url(self) -> str:
        if not self.subcategory_id or not self.subcategory.category_id:
            return reverse("frontpage_view")
        return reverse(
            "media_item_view",
            args=[self.subcategory.category.slug, self.subcategory.slug, self.slug],
        )

    def slug_siblings(self) -> models.QuerySet:
        return MediaItem.objects.filter(subcategory_id=self.subcategory_id)

    @property
    def preview_image(self):
        """У работы превью — её собственное изображение (общий шаблон карточки)."""
        return self.image

    @property
    def original_url(self) -> str:
        """Ссылка на оригинал: страница работы подменяет им лёгкую версию."""
        if not self.image:
            return ""
        return f"{self.image.url}?original=1"


class MediaItemReview(models.Model):
    """Комментарий пользователя к медиа-элементу."""

    media_item = models.ForeignKey(
        MediaItem,
        verbose_name=_("media item"),
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        related_name="reviews",
        on_delete=models.CASCADE,
    )
    content = models.TextField(_("content"), blank=True, default="")
    date_added = models.DateTimeField(_("date added"), auto_now_add=True, db_index=True)
    edited = models.BooleanField(_("edited"), default=False)

    class Meta:
        verbose_name = _("review")
        verbose_name_plural = _("reviews")
        ordering = ["-date_added"]
        indexes = [
            models.Index(fields=["media_item", "-date_added"], name="review_item_date_idx"),
        ]

    def __str__(self) -> str:
        return f"{self.media_item}, {self.user}"


class About(models.Model):
    """Единственная запись со страницей «О проекте» (переводится)."""

    body = models.TextField(_("body"), blank=True, default="")
    image = models.ImageField(_("image"), upload_to="about/", null=True, blank=True)

    class Meta:
        verbose_name = _("about page")
        verbose_name_plural = _("about page")

    def __str__(self) -> str:
        return "About"

    @classmethod
    def get_solo(cls) -> About | None:
        return cls.objects.first()


# ---------------------------------------------------------------------------
# Чистка файлов картинок
# ---------------------------------------------------------------------------
def _image_storage(model):
    return model._meta.get_field("image").storage


def _delete_stored_file(model, name: str) -> None:
    """Удаляет файл из хранилища, не роняя операцию при ошибке сети."""
    if not name:
        return
    try:
        _image_storage(model).delete(name)
    except Exception:  # noqa: BLE001 — удаление файла не должно ломать сохранение
        logger.warning("Не удалось удалить файл %s", name, exc_info=True)


def _delete_replaced_image(sender, instance, **kwargs) -> None:
    """Удаляет старый файл, если картинку заменили."""
    if not instance.pk:
        return
    old_name = sender.objects.filter(pk=instance.pk).values_list("image", flat=True).first() or ""
    new_name = instance.image.name if instance.image else ""
    if old_name and old_name != new_name:
        _delete_stored_file(sender, old_name)


def _delete_image_of_deleted_object(sender, instance, **kwargs) -> None:
    if instance.image and instance.image.name:
        _delete_stored_file(sender, instance.image.name)


for _model in (MediaItem, SubCategory, About):
    pre_save.connect(
        _delete_replaced_image,
        sender=_model,
        dispatch_uid=f"core.delete_replaced_image.{_model.__name__}",
    )
    post_delete.connect(
        _delete_image_of_deleted_object,
        sender=_model,
        dispatch_uid=f"core.delete_image_of_deleted_object.{_model.__name__}",
    )
