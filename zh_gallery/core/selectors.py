"""Селекторы — запросы на чтение.

Вся ORM-логика чтения собрана здесь, чтобы вьюхи оставались короткими, а
шаблоны не дёргали ``.count()`` на каждой карточке (N+1).
"""

from __future__ import annotations

from django.db.models import Count, IntegerField, OuterRef, Prefetch, QuerySet, Subquery, Sum
from django.db.models.functions import Coalesce

from .models import About, MainCategory, MediaItem, MediaItemReview, SubCategory


def get_categories() -> QuerySet[MainCategory]:
    """Категории для верхнего меню."""
    return MainCategory.objects.all()


def get_about() -> About | None:
    """Страница «О проекте» (может отсутствовать)."""
    return About.get_solo()


def subcategories_with_stats(category: MainCategory) -> QuerySet[SubCategory]:
    """Подкатегории категории вместе с суммарными просмотрами/лайками/отзывами."""
    total_views = (
        MediaItem.objects.filter(subcategory=OuterRef("pk"))
        # сбрасываем ordering модели: иначе modeltranslation добавляет title_ru
        # в GROUP BY и сумма считается по каждой группе отдельно
        .order_by()
        .values("subcategory")
        .annotate(total=Coalesce(Sum("views"), 0))
        .values("total")[:1]
    )
    return (
        SubCategory.objects.filter(category=category)
        .annotate(
            views_count=Coalesce(Subquery(total_views, output_field=IntegerField()), 0),
            likes_count=Count("media_items__likes", distinct=True),
            reviews_count=Count("media_items__reviews", distinct=True),
        )
        .order_by("title")
    )


def media_items_with_stats(subcategory: SubCategory) -> QuerySet[MediaItem]:
    """Медиа-элементы подкатегории с готовыми счётчиками."""
    return MediaItem.objects.with_stats().filter(subcategory=subcategory)


def media_item_neighbours(media_item: MediaItem) -> dict:
    """Соседи работы в её подкатегории — для перелистывания.

    Порядок совпадает с сеткой подкатегории (по названию), поэтому «следующая»
    работа визуально та же, что справа в списке.
    """
    siblings = MediaItem.objects.filter(subcategory_id=media_item.subcategory_id).order_by("title")
    ids = list(siblings.values_list("pk", flat=True))
    if media_item.pk not in ids:
        return {"prev_item": None, "next_item": None, "position": None, "total": len(ids)}

    index = ids.index(media_item.pk)
    prev_id = ids[index - 1] if index > 0 else None
    next_id = ids[index + 1] if index < len(ids) - 1 else None
    neighbours = {
        item.pk: item for item in siblings.filter(pk__in=[i for i in (prev_id, next_id) if i])
    }

    return {
        "prev_item": neighbours.get(prev_id),
        "next_item": neighbours.get(next_id),
        "position": index + 1,
        "total": len(ids),
    }


def last_reviews(limit: int = 10) -> QuerySet[MediaItemReview]:
    """Последние комментарии для главной."""
    return (
        MediaItemReview.objects.select_related("user")
        .prefetch_related(Prefetch("media_item", queryset=MediaItem.objects.with_stats()))
        .order_by("-date_added")[:limit]
    )


def recently_liked_items(limit: int = 10) -> QuerySet[MediaItem]:
    """Недавно лайкнутые элементы для главной."""
    return MediaItem.objects.with_stats().liked_recently()[:limit]


def reviews_of(user) -> QuerySet[MediaItemReview]:
    """Комментарии пользователя с подтянутыми элементами."""
    return user.reviews.select_related(
        "media_item",
        "media_item__subcategory",
        "media_item__subcategory__category",
    ).order_by("-date_added")


def liked_items_of(user) -> QuerySet[MediaItem]:
    """Элементы, которые пользователь лайкнул."""
    return user.liked_items.with_stats().order_by("title")


def all_image_names():
    """Все имена файлов, на которые ссылаются модели (для проверки и прогрева кэша)."""
    yield from MediaItem.objects.exclude(image="").order_by("pk").values_list("image", flat=True)
    yield from SubCategory.objects.exclude(image="").order_by("pk").values_list("image", flat=True)
    yield from About.objects.exclude(image="").values_list("image", flat=True)


def get_random_media_item() -> MediaItem | None:
    """Случайный элемент для Telegram-бота.

    ``order_by('?')`` — самый простой вариант; на больших таблицах его стоит
    заменить выборкой случайного pk в диапазоне.
    """
    return MediaItem.objects.with_stats().order_by("?").first()
