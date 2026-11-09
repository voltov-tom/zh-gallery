"""Тесты моделей: слаги, лайки, ссылки и удаление файлов."""

from __future__ import annotations

import pytest

from core.models import MediaItem, SubCategory
from core.tests.conftest_helpers import make_image_file


@pytest.mark.django_db
def test_slug_is_generated_from_title(category, subcategory, media_item):
    assert category.slug == "zhivopis"
    assert subcategory.slug == "portrety"
    assert media_item.slug == "tikhii-vzgliad"


@pytest.mark.django_db
def test_slug_does_not_change_when_title_changes(media_item):
    old_slug = media_item.slug
    media_item.title = "Совсем другое название"
    media_item.save()
    media_item.refresh_from_db()
    assert media_item.slug == old_slug


@pytest.mark.django_db
def test_slug_is_unique_within_parent(subcategory):
    first = MediaItem(subcategory=subcategory, title="Закат")
    first.image.save("a.jpg", make_image_file(), save=True)

    second = MediaItem(subcategory=subcategory, title="Закат!")
    second.image.save("b.jpg", make_image_file(), save=True)

    assert first.slug == "zakat"
    assert second.slug == "zakat-2"


@pytest.mark.django_db
def test_same_title_allowed_in_different_subcategories(category, subcategory):
    other_subcategory = SubCategory.objects.create(category=category, title="Пейзажи")

    first = MediaItem(subcategory=subcategory, title="Закат")
    first.image.save("a.jpg", make_image_file(), save=True)

    second = MediaItem(subcategory=other_subcategory, title="Закат")
    second.image.save("b.jpg", make_image_file(), save=True)

    assert first.slug == "zakat"
    assert second.slug == "zakat"
    assert first.pk != second.pk


@pytest.mark.django_db
def test_like_time_is_empty_until_first_like(media_item, user):
    assert media_item.like_time is None

    media_item.likes.add(user)
    media_item.like_time = None
    assert media_item.like_time is None


@pytest.mark.django_db
def test_like_time_does_not_change_on_regular_save(media_item):
    from django.utils import timezone

    moment = timezone.now()
    media_item.like_time = moment
    media_item.save()

    media_item.description = "новое описание"
    media_item.save()
    media_item.refresh_from_db()

    assert media_item.like_time == moment


@pytest.mark.django_db
def test_get_absolute_url_uses_reverse(media_item):
    assert media_item.get_absolute_url() == "/zhivopis/portrety/tikhii-vzgliad/"


@pytest.mark.django_db
def test_get_absolute_url_survives_orphan_item(subcategory):
    item = MediaItem(subcategory=subcategory, title="Без категории")
    item.image.save("c.jpg", make_image_file(), save=True)
    subcategory.category = None
    subcategory.save()

    assert item.get_absolute_url() == "/"


@pytest.mark.django_db
def test_image_file_removed_with_object(media_item):
    storage = media_item.image.storage
    name = media_item.image.name
    assert storage.exists(name)

    media_item.delete()
    assert not storage.exists(name)


@pytest.mark.django_db
def test_replaced_image_file_is_removed(media_item):
    storage = media_item.image.storage
    old_name = media_item.image.name

    media_item.image.save("new.jpg", make_image_file("new.jpg", (10, 20, 30)))
    media_item.refresh_from_db()

    assert not storage.exists(old_name)
    assert storage.exists(media_item.image.name)


@pytest.mark.django_db
def test_media_item_upload_path_uses_subcategory(subcategory):
    """Новые файлы раскладываются по папкам подкатегорий, а не по месяцам."""
    item = MediaItem(subcategory=subcategory, title="Проверка")

    name = item.image.field.generate_filename(item, "Первый кадр.JPG")

    assert name.startswith(f"{subcategory.category.slug}/{subcategory.slug}/"), name
    assert name.endswith(".jpg")
    assert " " not in name and "Первый" not in name


@pytest.mark.django_db
def test_reorganize_media_target_name_for_legacy_file(media_item):
    """Старый файл из корня получает путь подкатегории и slug-имя."""
    from core.management.commands.reorganize_media import target_name

    media_item.image.name = "ABC-123.JPEG"

    expected = f"{media_item.subcategory.category.slug}/{media_item.subcategory.slug}/abc-123.jpeg"
    assert target_name(media_item) == expected


@pytest.mark.django_db
def test_reorganize_media_skips_already_organized(media_item):
    """Файлы, уже лежащие в папке подкатегории, не трогаем."""
    from io import StringIO

    from django.core.management import call_command

    out = StringIO()
    call_command("reorganize_media", "--dry-run", stdout=out)

    assert "пропущено: 1" in out.getvalue()


@pytest.mark.django_db
def test_subcategory_preview_prefers_media_item(subcategory, media_item):
    """Превью подкатегории — выбранная работа, если она задана."""
    subcategory.preview_item = media_item
    subcategory.save(update_fields=["preview_item"])

    assert subcategory.preview_image == media_item.image


@pytest.mark.django_db
def test_subcategory_preview_falls_back_to_uploaded_image(subcategory, image_file):
    """Если работа не выбрана — используется загруженная картинка."""
    subcategory.image.save("preview.jpg", image_file(), save=True)
    subcategory.refresh_from_db()

    assert subcategory.preview_image.name == subcategory.image.name
