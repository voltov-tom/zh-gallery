"""Тесты сервисов: лайки и счётчик просмотров."""

from __future__ import annotations

import pytest

from core import services
from core.models import MediaItem


@pytest.mark.django_db
def test_register_view_increments_persistently(media_item):
    assert services.register_view(media_item) == 1
    assert services.register_view(media_item) == 2
    assert MediaItem.objects.get(pk=media_item.pk).views == 2


@pytest.mark.django_db
def test_toggle_like_sets_and_clears_like(media_item, user):
    assert services.toggle_like(media_item, user) is True
    assert media_item.likes.filter(pk=user.pk).exists()
    assert media_item.like_time is not None

    assert services.toggle_like(media_item, user) is False
    assert not media_item.likes.filter(pk=user.pk).exists()


@pytest.mark.django_db
def test_toggle_like_is_per_user(media_item, user, other_user):
    services.toggle_like(media_item, user)
    services.toggle_like(media_item, other_user)

    assert media_item.likes.count() == 2


@pytest.mark.django_db
def test_create_and_update_review_marks_it_edited(media_item, user):
    review = services.create_review(media_item, user, "  текст  ")
    assert review.content == "текст"
    assert review.edited is False

    services.update_review(review, "новый текст")
    review.refresh_from_db()
    assert review.content == "новый текст"
    assert review.edited is True


@pytest.mark.django_db
def test_update_review_with_same_content_does_not_mark_edited(media_item, user):
    review = services.create_review(media_item, user, "текст")

    services.update_review(review, "текст")

    review.refresh_from_db()
    assert review.edited is False
