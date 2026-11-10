"""Тесты селекторов: агрегаты и отсутствие N+1."""

from __future__ import annotations

import pytest

from core import selectors, services
from core.models import MediaItem, MediaItemReview
from core.tests.conftest_helpers import make_image_file


def _add_item(subcategory, title: str, views: int = 0) -> MediaItem:
    item = MediaItem(subcategory=subcategory, title=title)
    item.image.save(f"{title}.jpg", make_image_file(f"{title}.jpg"), save=True)
    if views:
        MediaItem.objects.filter(pk=item.pk).update(views=views)
        item.refresh_from_db(fields=["views"])
    return item


@pytest.mark.django_db
def test_subcategories_with_stats_aggregate_all_items(category, subcategory, user):
    first = _add_item(subcategory, "Первый", views=3)
    second = _add_item(subcategory, "Второй", views=4)
    first.likes.add(user)
    MediaItemReview.objects.create(media_item=second, user=user, content="ок")

    stats = selectors.subcategories_with_stats(category).get(pk=subcategory.pk)

    assert stats.views_count == 7
    assert stats.likes_count == 1
    assert stats.reviews_count == 1


@pytest.mark.django_db
def test_subcategories_with_stats_handles_empty_subcategory(category, subcategory):
    stats = selectors.subcategories_with_stats(category).get(pk=subcategory.pk)
    assert stats.views_count == 0
    assert stats.likes_count == 0
    assert stats.reviews_count == 0


@pytest.mark.django_db
def test_subcategories_stats_use_single_query(category, subcategory, django_assert_num_queries):
    _add_item(subcategory, "Первый", views=1)

    with django_assert_num_queries(1):
        list(selectors.subcategories_with_stats(category))


@pytest.mark.django_db
def test_media_items_with_stats_do_not_query_per_card(subcategory, user, django_assert_num_queries):
    item = _add_item(subcategory, "Первый", views=2)
    item.likes.add(user)
    MediaItemReview.objects.create(media_item=item, user=user, content="ок")

    with django_assert_num_queries(1):
        items = list(selectors.media_items_with_stats(subcategory))
        assert items[0].likes_count == 1
        assert items[0].reviews_count == 1
        assert items[0].views == 2


@pytest.mark.django_db
def test_recently_liked_items_ignore_never_liked(media_item, subcategory, user):
    MediaItem.objects.create(subcategory=subcategory, title="Без лайка")
    MediaItem.objects.filter(pk=media_item.pk).update(views=0)
    services.toggle_like(media_item, user)

    titles = [item.title for item in selectors.recently_liked_items()]
    assert titles == [media_item.title]


@pytest.mark.django_db
def test_last_reviews_prefetch_media_item_stats(media_item, user, django_assert_num_queries):
    MediaItemReview.objects.create(media_item=media_item, user=user, content="ок")

    with django_assert_num_queries(2):
        reviews = list(selectors.last_reviews())
        assert reviews[0].media_item.likes_count == 0
        assert reviews[0].media_item.reviews_count == 1


@pytest.mark.django_db
def test_get_random_media_item_returns_none_for_empty_gallery(db):
    assert selectors.get_random_media_item() is None


@pytest.mark.django_db
def test_media_item_neighbours_follow_title_order(subcategory, media_item):
    """Соседи считаются по тому же порядку, что и сетка, — по названию."""
    from core.models import MediaItem
    from core.selectors import media_item_neighbours

    later = MediaItem.objects.create(subcategory=subcategory, title="Яблочный сад")
    earlier = MediaItem.objects.create(subcategory=subcategory, title="Апрель")

    middle = media_item_neighbours(media_item)
    assert middle["prev_item"] == earlier
    assert middle["next_item"] == later
    assert middle["position"] == 2
    assert middle["total"] == 3

    first = media_item_neighbours(earlier)
    assert first["prev_item"] is None
    assert first["position"] == 1

    last = media_item_neighbours(later)
    assert last["next_item"] is None
    assert last["position"] == 3
