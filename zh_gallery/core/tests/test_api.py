"""Тесты JSON API лайков и комментариев."""

from __future__ import annotations

import json

import pytest
from django.urls import reverse

from core.models import MediaItemReview


def post_json(client, url, payload):
    return client.post(url, data=json.dumps(payload), content_type="application/json")


@pytest.mark.django_db
def test_like_toggles_on_and_off(client, media_item, user):
    client.force_login(user)
    url = reverse("like_button")

    first = post_json(client, url, {"media_id": media_item.pk})
    assert first.status_code == 200
    assert first.json() == {
        "success": True,
        "liked": True,
        "likes_count": 1,
        "media_id": media_item.pk,
    }

    media_item.refresh_from_db()
    assert media_item.like_time is not None
    assert media_item.likes.filter(pk=user.pk).exists()

    second = post_json(client, url, {"media_id": media_item.pk})
    assert second.json()["liked"] is False
    assert second.json()["likes_count"] == 0
    assert not media_item.likes.filter(pk=user.pk).exists()


@pytest.mark.django_db
def test_like_accepts_legacy_operation_field(client, media_item, user):
    client.force_login(user)

    response = post_json(
        client, reverse("like_button"), {"media_id": media_item.pk, "operation": "like_submit"}
    )

    assert response.json()["success"] is True


@pytest.mark.django_db
def test_like_requires_authentication(client, media_item):
    response = post_json(client, reverse("like_button"), {"media_id": media_item.pk})

    assert response.status_code == 403
    assert response.json()["success"] is False


@pytest.mark.django_db
def test_like_requires_post(client, media_item, user):
    client.force_login(user)

    assert client.get(reverse("like_button")).status_code == 405


@pytest.mark.django_db
def test_like_rejects_broken_json(client, user):
    client.force_login(user)

    response = client.post(
        reverse("like_button"), data="{not json", content_type="application/json"
    )

    assert response.status_code == 400
    assert response.json()["success"] is False


@pytest.mark.django_db
def test_like_rejects_missing_media_id(client, user):
    client.force_login(user)

    response = post_json(client, reverse("like_button"), {})

    assert response.status_code == 400


@pytest.mark.django_db
def test_like_returns_404_for_unknown_item(client, user):
    client.force_login(user)

    response = post_json(client, reverse("like_button"), {"media_id": 999999})

    assert response.status_code == 404


@pytest.mark.django_db
def test_edit_review_updates_own_comment(client, review, user):
    client.force_login(user)

    response = post_json(
        client, reverse("edit_review"), {"review_id": review.pk, "content": "  исправлено  "}
    )

    review.refresh_from_db()
    assert response.status_code == 200
    assert response.json() == {"success": True, "edited": True, "content": "исправлено"}
    assert review.content == "исправлено"
    assert review.edited is True


@pytest.mark.django_db
def test_edit_review_keeps_edited_flag_when_content_is_same(client, review, user):
    client.force_login(user)

    post_json(client, reverse("edit_review"), {"review_id": review.pk, "content": review.content})

    review.refresh_from_db()
    assert review.edited is False


@pytest.mark.django_db
def test_edit_review_rejects_empty_content(client, review, user):
    client.force_login(user)

    response = post_json(client, reverse("edit_review"), {"review_id": review.pk, "content": "   "})

    assert response.status_code == 400
    assert MediaItemReview.objects.get(pk=review.pk).content == review.content


@pytest.mark.django_db
def test_edit_review_of_another_user_is_404(client, review, other_user):
    client.force_login(other_user)

    response = post_json(
        client, reverse("edit_review"), {"review_id": review.pk, "content": "чужой"}
    )

    assert response.status_code == 404
    review.refresh_from_db()
    assert review.content == "Первый комментарий"


@pytest.mark.django_db
def test_delete_review_removes_own_comment(client, review, user):
    client.force_login(user)

    response = post_json(client, reverse("delete_review"), {"review_id": review.pk})

    assert response.status_code == 200
    assert response.json()["success"] is True
    assert not MediaItemReview.objects.filter(pk=review.pk).exists()


@pytest.mark.django_db
def test_delete_review_of_another_user_is_404(client, review, other_user):
    client.force_login(other_user)

    response = post_json(client, reverse("delete_review"), {"review_id": review.pk})

    assert response.status_code == 404
    assert MediaItemReview.objects.filter(pk=review.pk).exists()


@pytest.mark.django_db
def test_delete_review_requires_authentication(client, review):
    response = post_json(client, reverse("delete_review"), {"review_id": review.pk})

    assert response.status_code == 403
    assert MediaItemReview.objects.filter(pk=review.pk).exists()
