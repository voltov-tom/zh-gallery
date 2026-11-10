"""Тесты локального кэша медиа: отдача при упавшем WebDAV и заглушка."""

from __future__ import annotations

import io

import pytest
from django.core.management import call_command
from django.urls import reverse

from core import media_cache

JPEG = b"\xff\xd8\xff\xe0" + b"\x00" * 32
MEDIA_NAME = "media_items/test/pic.jpg"


class FakeStorage:
    """Подменяет default_storage: отдаёт заданные файлы, считает обращения."""

    def __init__(self, files: dict[str, bytes]):
        self.files = files
        self.opened = 0

    def open(self, name, mode="rb"):
        self.opened += 1
        if name not in self.files:
            raise FileNotFoundError(name)
        return io.BytesIO(self.files[name])


@pytest.fixture
def cache_dir(settings, tmp_path):
    settings.MEDIA_CACHE_ENABLED = True
    settings.MEDIA_CACHE_ROOT = tmp_path / "media-cache"
    return settings.MEDIA_CACHE_ROOT


@pytest.fixture
def fake_storage(monkeypatch):
    def install(files):
        storage = FakeStorage(files)
        monkeypatch.setattr("core.views.media.default_storage", storage)
        return storage

    return install


@pytest.mark.django_db
def test_download_is_cached_and_second_request_hits_cache(client, cache_dir, fake_storage):
    storage = fake_storage({MEDIA_NAME: JPEG})

    first = client.get(reverse("media_file", args=[MEDIA_NAME]))
    second = client.get(reverse("media_file", args=[MEDIA_NAME]))

    assert first.status_code == 200
    assert first["X-Media-Cache"] == "miss"
    assert second["X-Media-Cache"] == "hit"
    assert storage.opened == 1, "файл должен скачиваться из хранилища один раз"
    assert media_cache.read(MEDIA_NAME) is not None


@pytest.mark.django_db
def test_cached_file_is_served_when_storage_is_down(client, cache_dir, fake_storage):
    fake_storage({MEDIA_NAME: JPEG})
    client.get(reverse("media_file", args=[MEDIA_NAME]))

    # «WebDAV упал»: любое обращение к хранилищу теперь падает
    fake_storage({})

    response = client.get(reverse("media_file", args=[MEDIA_NAME]))

    assert response.status_code == 200
    assert response["X-Media-Cache"] == "hit"
    assert b"".join(response.streaming_content) == JPEG


@pytest.mark.django_db
def test_missing_file_falls_back_to_placeholder(client, cache_dir, fake_storage):
    fake_storage({})

    response = client.get(reverse("media_file", args=["media_items/gone.jpg"]))

    assert response.status_code == 302
    assert response["X-Media-Placeholder"] == "1"
    assert "no_photo.jpeg" in response["Location"]


@pytest.mark.django_db
def test_empty_file_falls_back_to_placeholder(client, cache_dir, fake_storage):
    fake_storage({MEDIA_NAME: b""})

    response = client.get(reverse("media_file", args=[MEDIA_NAME]))

    assert response.status_code == 302
    assert response["X-Media-Placeholder"] == "1"


@pytest.mark.django_db
def test_cache_is_disabled_without_setting(client, settings, fake_storage, tmp_path):
    settings.MEDIA_CACHE_ENABLED = False
    settings.MEDIA_CACHE_ROOT = tmp_path / "media-cache"
    fake_storage({MEDIA_NAME: JPEG})

    response = client.get(reverse("media_file", args=[MEDIA_NAME]))

    assert response.status_code == 200
    assert response["X-Media-Cache"] == "miss"
    assert not media_cache.cache_root()


def test_cache_path_rejects_traversal(cache_dir):
    assert media_cache.cache_path("../secret.txt") is None
    assert media_cache.cache_path("a/../../secret.txt") is None
    assert media_cache.cache_path("media/pic.jpg") is not None


def test_store_and_clear(cache_dir):
    media_cache.store("a/b.jpg", JPEG)
    media_cache.store("c.jpg", JPEG)

    assert media_cache.stats() == (2, len(JPEG) * 2)
    assert media_cache.clear() == 2
    assert media_cache.read("a/b.jpg") is None


@pytest.mark.django_db
def test_warm_command_fills_cache(cache_dir, media_item, capsys):
    call_command("media_cache", verbosity=0)

    assert media_cache.read(media_item.image.name) is not None
    assert "добавлено: 1" in capsys.readouterr().out

    call_command("media_cache", verbosity=0)
    assert "Уже было в кэше: 1" in capsys.readouterr().out


@pytest.mark.django_db
def test_warm_command_reports_missing_file(cache_dir, media_item, capsys):
    media_item.image.storage.delete(media_item.image.name)

    call_command("media_cache", verbosity=0)

    captured = capsys.readouterr()
    assert "нет в хранилище" in captured.out
    assert "Недоступных файлов: 1" in captured.err


@pytest.mark.django_db
def test_warm_command_disabled(settings, capsys):
    settings.MEDIA_CACHE_ENABLED = False

    call_command("media_cache", verbosity=0)

    assert "Кэш медиа выключен" in capsys.readouterr().err


def test_cache_keeps_web_and_original_separately(cache_dir):
    """Лёгкая версия и оригинал лежат в разных подкаталогах."""
    from core import media_cache

    media_cache.store("pic.jpg", b"web-bytes", "web")
    media_cache.store("pic.jpg", b"original-bytes", "orig")

    assert media_cache.read("pic.jpg", "web").read_bytes() == b"web-bytes"
    assert media_cache.read("pic.jpg", "orig").read_bytes() == b"original-bytes"
