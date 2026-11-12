"""Тесты безопасности: то, что легко сломать незаметно."""

from __future__ import annotations

import json
import pathlib
import subprocess

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


@pytest.mark.parametrize(
    "conf",
    ["docker/nginx.conf", "docker/nginx-nextcloud.conf", "deploy/nginx-prod.conf"],
)
def test_nginx_hides_version(conf):
    config = (REPO_DIR / conf).read_text()

    assert "server_tokens off;" in config


def test_nginx_rate_limits_admin_login():
    """Перебор пароля в админке режет nginx: сам django-admin лимитов не имеет."""
    config = (REPO_DIR / "deploy/nginx-prod.conf").read_text()

    assert "limit_req_zone" in config
    assert "limit_req zone=admin" in config
    assert "location ~ ^/admin/" in config


def test_deploy_reloads_nginx_after_config_sync():
    """Конфиг монтируется файлом: без reload контейнер живёт со старыми правилами."""
    script = (REPO_DIR / "deploy/deploy.sh").read_text()

    assert "nginx -t" in script
    assert "nginx -s reload" in script
    # сначала проверка конфига, только потом reload
    assert script.index("nginx -t") < script.index("nginx -s reload")


def _run_botctl(*args: str) -> subprocess.CompletedProcess:
    script = REPO_DIR / "deploy" / "ops" / "zhbotctl-root"
    return subprocess.run(["sh", str(script), *args], capture_output=True, text=True, check=False)


def test_zhctl_root_routes_bot_commands_to_its_own_script():
    """Стек бота обслуживает отдельный скрипт — значит, и whitelist отдельный."""
    script = (REPO_DIR / "deploy/ops/zhctl-root").read_text()

    assert "zhbotctl-root" in script
    assert "bot\\ *)" in script


def test_bot_deploy_accepts_only_full_sha():
    """Короткий, неполный и не-hex sha отбиваются до запуска docker."""
    for bad in ("deploy ", "deploy abc", "deploy " + "z" * 40):
        result = _run_botctl(bad)
        assert result.returncode == 2, bad
        assert "sha" in result.stderr

    # «deploy» без аргумента — вообще не разрешённая команда
    assert _run_botctl("deploy").returncode == 1


def test_bot_deploy_rejects_unknown_commands():
    result = _run_botctl("rm -rf /")

    assert result.returncode == 1
    assert "не разрешена" in result.stderr


def test_dockerfile_runs_as_non_root_user():
    dockerfile = (REPO_DIR / "Dockerfile").read_text()

    assert "USER app" in dockerfile
    assert "useradd" in dockerfile


@pytest.mark.django_db
def test_telegram_api_is_disabled_without_token(client, media_item, settings):
    """Без TELEGRAM_BOT_TOKEN эндпоинты выключены: иначе накручиваются просмотры."""
    settings.TELEGRAM_BOT_TOKEN = ""
    views_before = media_item.views

    response = client.get(reverse("get_media_item", args=[media_item.slug]))

    assert response.status_code == 403
    media_item.refresh_from_db()
    assert media_item.views == views_before


@pytest.mark.django_db
def test_telegram_api_requires_correct_token(client, media_item, settings):
    settings.TELEGRAM_BOT_TOKEN = "secret-bot-token"

    forbidden = client.get(reverse("get_media_item", args=[media_item.slug]))
    allowed = client.get(
        reverse("get_media_item", args=[media_item.slug]),
        headers={"X-Bot-Token": "secret-bot-token"},
    )

    assert forbidden.status_code == 403
    assert allowed.status_code == 200
    assert allowed.json()["title"] == media_item.title


@pytest.mark.django_db
def test_telegram_api_rejects_wrong_length_token(client, media_item, settings):
    """Токен сравнивается за постоянное время и не падает на другой длине."""
    settings.TELEGRAM_BOT_TOKEN = "secret-bot-token"

    response = client.get(
        reverse("get_media_item", args=[media_item.slug]),
        headers={"X-Bot-Token": "short"},
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_telegram_random_item_is_disabled_without_token(client, media_item, settings):
    settings.TELEGRAM_BOT_TOKEN = ""

    response = client.get(reverse("get_random_item"))

    assert response.status_code == 403
