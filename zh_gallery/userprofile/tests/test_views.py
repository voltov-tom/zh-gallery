"""Тесты личного кабинета."""

from __future__ import annotations

import pytest
from django.urls import reverse

from core.models import MediaItemReview


@pytest.mark.django_db
def test_my_account_requires_login(client):
    response = client.get(reverse("my_account_view"))

    assert response.status_code == 302
    assert reverse("account_login") in response["Location"]


@pytest.mark.django_db
def test_my_account_shows_own_reviews_and_edit_controls(client, user, review):
    client.force_login(user)

    response = client.get(reverse("my_account_view"))

    assert response.status_code == 200
    assert review.content.encode() in response.content
    assert b"data-review-item" in response.content
    assert b"data-review-textarea" in response.content


@pytest.mark.django_db
def test_other_profile_is_read_only(client, user, other_user, review):
    client.force_login(other_user)

    response = client.get(reverse("account_view", args=[user.username]))

    assert response.status_code == 200
    assert review.content.encode() in response.content
    assert b"data-review-textarea" not in response.content
    assert b"data-review-item" in response.content


@pytest.mark.django_db
def test_own_profile_redirects_to_my_account(client, user):
    client.force_login(user)

    response = client.get(reverse("account_view", args=[user.username]))

    assert response.status_code == 302
    assert response["Location"] == reverse("my_account_view")


@pytest.mark.django_db
def test_unknown_profile_is_404(client):
    assert client.get(reverse("account_view", args=["ghost"])).status_code == 404


@pytest.mark.django_db
def test_liked_items_are_listed_in_account(client, user, media_item):
    media_item.likes.add(user)
    client.force_login(user)

    response = client.get(reverse("my_account_view"))

    assert media_item.title.encode() in response.content


@pytest.mark.django_db
def test_reviews_are_escaped_in_profile(client, user, media_item):
    MediaItemReview.objects.create(
        media_item=media_item, user=user, content="<img src=x onerror=alert(1)>"
    )
    client.force_login(user)

    response = client.get(reverse("my_account_view"))

    assert b"<img src=x onerror=alert(1)>" not in response.content
    assert b"&lt;img" in response.content


@pytest.mark.django_db
def test_profile_does_not_duplicate_queries_per_review(
    client, user, media_item, django_assert_max_num_queries
):
    for index in range(3):
        MediaItemReview.objects.create(media_item=media_item, user=user, content=f"отзыв {index}")
    client.force_login(user)

    with django_assert_max_num_queries(12):
        response = client.get(reverse("my_account_view"))

    assert response.status_code == 200
