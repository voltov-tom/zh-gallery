"""Тесты генерации описаний через ИИ (API замокан, наружу не ходим)."""

from __future__ import annotations

import json

import pytest
from django.urls import reverse

from core.integrations import ai
from core.services import generate_media_description


class FakeResponse:
    def __init__(self, payload: dict | None = None, status_code: int = 200):
        self.status_code = status_code
        self._payload = payload or {}
        self.text = json.dumps(self._payload)

    def json(self) -> dict:
        return self._payload


def make_api_response(content: str) -> FakeResponse:
    return FakeResponse({"choices": [{"message": {"content": content}}]})


@pytest.fixture
def ai_settings(settings):
    settings.AI_API_KEY = "test-key"
    settings.AI_MODEL = "deepseek-flash"
    settings.AI_BASE_URL = "https://api.example.com"
    settings.AI_TIMEOUT = 5
    settings.AI_MAX_TOKENS = 1000
    return settings


def test_generate_description_saves_both_languages(media_item, ai_settings, monkeypatch):
    payload = json.dumps({"ru": "Мягкий свет и тёплая стена.", "en": "Soft light and a warm wall."})
    monkeypatch.setattr(ai.requests, "post", lambda *a, **kw: make_api_response(f"```json\n{payload}\n```"))

    texts = generate_media_description(media_item)

    media_item.refresh_from_db()
    assert texts == {"ru": "Мягкий свет и тёплая стена.", "en": "Soft light and a warm wall."}
    assert media_item.description_ru == "Мягкий свет и тёплая стена."
    assert media_item.description_en == "Soft light and a warm wall."


def test_generate_description_truncates_to_field_length(media_item, ai_settings, monkeypatch):
    long_text = "ж" * 400
    payload = json.dumps({"ru": long_text, "en": long_text})
    monkeypatch.setattr(ai.requests, "post", lambda *a, **kw: make_api_response(payload))

    generate_media_description(media_item)

    media_item.refresh_from_db()
    assert len(media_item.description_ru) == ai.MAX_DESCRIPTION_LENGTH
    assert len(media_item.description_en) == ai.MAX_DESCRIPTION_LENGTH


def test_generate_description_requires_key(media_item, settings):
    settings.AI_API_KEY = ""

    with pytest.raises(ai.AIDescriptionError, match="AI_API_KEY"):
        generate_media_description(media_item)


def test_api_error_keeps_old_description(media_item, ai_settings, monkeypatch):
    media_item.description_ru = "старое описание"
    media_item.save(update_fields=["description_ru"])
    monkeypatch.setattr(ai.requests, "post", lambda *a, **kw: FakeResponse({"error": "boom"}, 500))

    with pytest.raises(ai.AIDescriptionError):
        generate_media_description(media_item)

    media_item.refresh_from_db()
    assert media_item.description_ru == "старое описание"


def test_response_without_required_field_is_rejected(media_item, ai_settings, monkeypatch):
    payload = json.dumps({"ru": "только по-русски"})
    monkeypatch.setattr(ai.requests, "post", lambda *a, **kw: make_api_response(payload))

    with pytest.raises(ai.AIDescriptionError):
        generate_media_description(media_item)


@pytest.mark.django_db
def test_admin_button_generates_description(client, admin_user, media_item, ai_settings, monkeypatch):
    payload = json.dumps({"ru": "Описание из админки.", "en": "Description from admin."})
    monkeypatch.setattr(ai.requests, "post", lambda *a, **kw: make_api_response(payload))
    client.force_login(admin_user)

    response = client.get(
        reverse("admin:core_mediaitem_generate_description", args=[media_item.pk])
    )

    assert response.status_code == 302
    media_item.refresh_from_db()
    assert media_item.description_ru == "Описание из админки."


@pytest.mark.django_db
def test_admin_button_returns_json_for_ajax(client, admin_user, media_item, ai_settings, monkeypatch):
    payload = json.dumps({"ru": "Текст из AJAX.", "en": "Text from AJAX."})
    monkeypatch.setattr(ai.requests, "post", lambda *a, **kw: make_api_response(payload))
    client.force_login(admin_user)

    response = client.get(
        reverse("admin:core_mediaitem_generate_description", args=[media_item.pk]),
        headers={"X-Requested-With": "XMLHttpRequest"},
    )

    assert response.status_code == 200
    assert response.json() == {"success": True, "ru": "Текст из AJAX.", "en": "Text from AJAX."}


@pytest.mark.django_db
def test_admin_button_reports_error_in_json(client, admin_user, media_item, ai_settings, monkeypatch):
    monkeypatch.setattr(ai.requests, "post", lambda *a, **kw: FakeResponse({"error": "boom"}, 500))
    client.force_login(admin_user)

    response = client.get(
        reverse("admin:core_mediaitem_generate_description", args=[media_item.pk]),
        headers={"X-Requested-With": "XMLHttpRequest"},
    )

    assert response.status_code == 400
    assert response.json()["success"] is False


@pytest.mark.django_db
def test_admin_button_is_placed_before_description(client, admin_user, media_item, ai_settings):
    client.force_login(admin_user)

    html = client.get(f"/admin/core/mediaitem/{media_item.pk}/change/").content.decode()

    assert "Сгенерировать описание" in html
    assert html.index("Сгенерировать описание") < html.index('id="id_description_ru"')


@pytest.mark.django_db
def test_admin_add_form_has_no_button(client, admin_user, ai_settings):
    client.force_login(admin_user)

    html = client.get("/admin/core/mediaitem/add/").content.decode()

    assert "Сгенерировать описание" not in html


@pytest.mark.django_db
def test_admin_generate_response_is_not_cached(client, admin_user, media_item, ai_settings, monkeypatch):
    """Повторное нажатие не должно получать закэшированный ответ."""
    payload = json.dumps({"ru": "Новый текст.", "en": "New text."})
    monkeypatch.setattr(ai.requests, "post", lambda *a, **kw: make_api_response(payload))
    client.force_login(admin_user)

    response = client.get(
        reverse("admin:core_mediaitem_generate_description", args=[media_item.pk]),
        headers={"X-Requested-With": "XMLHttpRequest"},
    )

    cache_control = response.headers.get("Cache-Control", "")
    assert "no-store" in cache_control or "no-cache" in cache_control


@pytest.mark.django_db
def test_second_generation_overwrites_description(client, admin_user, media_item, ai_settings, monkeypatch):
    """Повторное нажатие перезаписывает уже существующее описание."""
    media_item.description_ru = "старое описание"
    media_item.description_en = "old description"
    media_item.save(update_fields=["description_ru", "description_en"])
    client.force_login(admin_user)

    texts = iter(
        [
            json.dumps({"ru": "первое новое", "en": "first new"}),
            json.dumps({"ru": "второе новое", "en": "second new"}),
        ]
    )
    monkeypatch.setattr(ai.requests, "post", lambda *a, **kw: make_api_response(next(texts)))

    url = reverse("admin:core_mediaitem_generate_description", args=[media_item.pk])
    client.get(url, headers={"X-Requested-With": "XMLHttpRequest"})
    client.get(url, headers={"X-Requested-With": "XMLHttpRequest"})

    media_item.refresh_from_db()
    assert media_item.description_ru == "второе новое"


@pytest.mark.django_db
def test_description_fields_are_textareas(client, admin_user, media_item, ai_settings):
    """Описания — многострочные поля, иначе 255 символов не видно."""
    client.force_login(admin_user)

    html = client.get(f"/admin/core/mediaitem/{media_item.pk}/change/").content.decode()

    assert '<textarea name="description_ru"' in html
    assert '<textarea name="description_en"' in html


@pytest.mark.django_db
def test_generation_marks_description_as_ai(media_item, ai_settings, monkeypatch):
    payload = json.dumps({"ru": "Текст.", "en": "Text."})
    monkeypatch.setattr(ai.requests, "post", lambda *a, **kw: make_api_response(payload))

    generate_media_description(media_item)

    media_item.refresh_from_db()
    assert media_item.description_generated_by_ai is True
