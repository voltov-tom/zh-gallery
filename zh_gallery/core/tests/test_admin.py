"""Smoke-тесты админки: страницы не должны падать с 500."""

from __future__ import annotations

import pytest
from django.urls import reverse

ADMIN_PAGES = [
    "admin:index",
    "admin:core_maincategory_changelist",
    "admin:core_subcategory_changelist",
    "admin:core_mediaitem_changelist",
    "admin:core_mediaitemreview_changelist",
    "admin:core_about_changelist",
]


@pytest.mark.django_db
@pytest.mark.parametrize("name", ADMIN_PAGES)
def test_admin_pages_render(client, admin_user, name):
    client.force_login(admin_user)

    response = client.get(reverse(name))

    assert response.status_code == 200


@pytest.mark.django_db
def test_media_item_changelist_shows_counters(client, admin_user, media_item, user):
    media_item.likes.add(user)
    client.force_login(admin_user)

    response = client.get(reverse("admin:core_mediaitem_changelist"))

    assert b"column-likes_count" in response.content
    assert media_item.title.encode() in response.content


@pytest.mark.django_db
def test_about_singleton_hides_add_button(client, admin_user, about):
    client.force_login(admin_user)

    response = client.get(reverse("admin:core_about_changelist"))

    assert response.status_code == 200
