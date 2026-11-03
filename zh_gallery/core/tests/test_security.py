"""Тесты безопасности: то, что легко сломать незаметно."""

from __future__ import annotations

import json
import pathlib

import pytest
from django.conf import settings
from django.test import Client
from django.urls import reverse

REPO_DIR = pathlib.Path(settings.BASE_DIR).parent


def test_csrf_cookie_is_not_readable_from_js():
    """Токен передаётся через <meta name="csrf-token">, cookie JS не нужен."""
    assert settings.CSRF_COOKIE_HTTPONLY is True


def test_session_cookie_is_httponly():
    assert settings.SESSION_COOKIE_HTTPONLY is True


def test_secure_proxy_header_is_set():
    """За nginx сайт должен понимать, что запрос пришёл по HTTPS."""
    assert settings.SECURE_PROXY_SSL_HEADER == ("HTTP_X_FORWARDED_PROTO", "https")


def test_json_api_requires_csrf_token():
    csrf_client = Client(enforce_csrf_checks=True)
    response = csrf_client.post(
        reverse("like_button"), data=json.dumps({"media_id": 1}), content_type="application/json"
    )

    assert response.status_code == 403


def test_admin_requires_authentication(client):
    response = client.get("/admin/")

    assert response.status_code == 302
    assert "/admin/login/" in response["Location"]


@pytest.mark.django_db
def test_healthz_does_not_leak_details(client):
    response = client.get(reverse("healthcheck"))

    assert response.json() == {"status": "ok", "database": "ok"}


@pytest.mark.parametrize("conf", ["docker/nginx.conf", "docker/nginx-nextcloud.conf"])
def test_nginx_hides_version(conf):
    config = (REPO_DIR / conf).read_text()

    assert "server_tokens off;" in config


def test_dockerfile_runs_as_non_root_user():
    dockerfile = (REPO_DIR / "Dockerfile").read_text()

    assert "USER app" in dockerfile
    assert "useradd" in dockerfile
