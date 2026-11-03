"""Тесты Telegram API."""

from __future__ import annotations

import pytest
from django.urls import reverse

from core.models import MediaItem

BOT_TOKEN = "test-bot-token"
BOT_HEADERS = {"X-Bot-Token": BOT_TOKEN}


@pytest.fixture(autouse=True)
def bot_token(settings):
    """Эндпоинты работают только с настроенным токеном (fail closed)."""
    settings.TELEGRAM_BOT_TOKEN = BOT_TOKEN


@pytest.mark.django_db
def test_random_item_returns_payload_and_counts_view(client, media_item):
    response = client.get(reverse("get_random_item"), headers=BOT_HEADERS)

    media_item.refresh_from_db()
    assert response.status_code == 200
    assert response.json()["title"] == media_item.title
    assert response.json()["views"] == 1
    assert media_item.views == 1
    assert response.json()["mediaItemUrl"].startswith("http://testserver/media/")


@pytest.mark.django_db
def test_random_item_404_for_empty_gallery(client):
    response = client.get(reverse("get_random_item"), headers=BOT_HEADERS)

    assert response.status_code == 404
    assert response.json()["success"] is False


@pytest.mark.django_db
def test_get_media_item_by_slug(client, media_item):
    response = client.get(reverse("get_media_item", args=[media_item.slug]), headers=BOT_HEADERS)

    media_item.refresh_from_db()
    assert response.status_code == 200
    assert response.json()["likes"] == 0
    assert media_item.views == 1


@pytest.mark.django_db
def test_get_media_item_404(client):
    response = client.get(reverse("get_media_item", args=["nope"]), headers=BOT_HEADERS)
    assert response.status_code == 404


@pytest.mark.django_db
def test_token_is_enforced(client, media_item):
    forbidden = client.get(reverse("get_random_item"))
    wrong = client.get(reverse("get_random_item"), headers={"X-Bot-Token": "wrong"})
    allowed = client.get(reverse("get_random_item"), headers=BOT_HEADERS)

    assert forbidden.status_code == 403
    assert wrong.status_code == 403
    assert allowed.status_code == 200


@pytest.mark.django_db
def test_view_counter_is_persisted_once(client, media_item):
    client.get(reverse("get_media_item", args=[media_item.slug]), headers=BOT_HEADERS)
    client.get(reverse("get_media_item", args=[media_item.slug]), headers=BOT_HEADERS)

    media_item.refresh_from_db()
    assert media_item.views == 2
    assert MediaItem.objects.get(pk=media_item.pk).views == 2
