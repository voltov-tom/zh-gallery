"""Тесты Telegram API."""

from __future__ import annotations

import json

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


@pytest.fixture(autouse=True)
def clear_cache():
    """Лимит отправок живёт в кэше — иначе тесты влияют друг на друга."""
    from django.core.cache import cache

    cache.clear()
    yield
    cache.clear()


def _contact_payload(**overrides):
    payload = {"text": "Привет, мне нравится галерея", "telegram_id": 4242, "username": "neo"}
    payload.update(overrides)
    return json.dumps(payload)


@pytest.mark.django_db
def test_contact_message_requires_token(client, mailoutbox):
    response = client.post(
        reverse("telegram_bot_send_message"),
        data=_contact_payload(),
        content_type="application/json",
    )

    assert response.status_code == 403
    assert mailoutbox == []


@pytest.mark.django_db
def test_contact_message_sends_email(client, mailoutbox, settings):
    response = client.post(
        reverse("telegram_bot_send_message"),
        data=_contact_payload(),
        content_type="application/json",
        headers=BOT_HEADERS,
    )

    assert response.status_code == 200
    assert response.json() == {"success": True}
    assert len(mailoutbox) == 1
    letter = mailoutbox[0]
    assert letter.to == [settings.CONTACT_EMAIL]
    assert "Привет, мне нравится галерея" in letter.body
    assert "@neo" in letter.subject
    assert "4242" in letter.body


@pytest.mark.django_db
def test_contact_message_without_username(client, mailoutbox):
    response = client.post(
        reverse("telegram_bot_send_message"),
        data=_contact_payload(username=""),
        content_type="application/json",
        headers=BOT_HEADERS,
    )

    assert response.status_code == 200
    assert "id 4242" in mailoutbox[0].subject


@pytest.mark.django_db
@pytest.mark.parametrize(
    "payload",
    [
        {"text": "", "telegram_id": 1},
        {"text": "   ", "telegram_id": 1},
        {"text": "x" * 2001, "telegram_id": 1},
        {"text": "привет", "telegram_id": "not-a-number"},
        {"text": "привет", "telegram_id": -5},
    ],
)
def test_contact_message_validation(client, mailoutbox, payload):
    response = client.post(
        reverse("telegram_bot_send_message"),
        data=json.dumps(payload),
        content_type="application/json",
        headers=BOT_HEADERS,
    )

    assert response.status_code == 400
    assert mailoutbox == []


@pytest.mark.django_db
def test_contact_message_rate_limited(client, mailoutbox):
    for _ in range(3):
        response = client.post(
            reverse("telegram_bot_send_message"),
            data=_contact_payload(),
            content_type="application/json",
            headers=BOT_HEADERS,
        )
        assert response.status_code == 200

    response = client.post(
        reverse("telegram_bot_send_message"),
        data=_contact_payload(),
        content_type="application/json",
        headers=BOT_HEADERS,
    )

    assert response.status_code == 429
    assert len(mailoutbox) == 3


@pytest.mark.django_db
def test_contact_message_breaks_header_injection(client, mailoutbox):
    response = client.post(
        reverse("telegram_bot_send_message"),
        data=_contact_payload(username="evil\nBcc: someone@example.com"),
        content_type="application/json",
        headers=BOT_HEADERS,
    )

    assert response.status_code == 200
    assert "\n" not in mailoutbox[0].subject
