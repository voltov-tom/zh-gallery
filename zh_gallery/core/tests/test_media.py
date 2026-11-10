"""Тесты отдачи медиа через Django (режим Nextcloud)."""

from __future__ import annotations

import pytest
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.urls import reverse

from core.views.media import media_file

JPEG = b"\xff\xd8\xff" + b"\x00" * 32


@pytest.fixture
def stored_file():
    name = "media_items/test/pic.jpg"
    default_storage.save(name, ContentFile(JPEG))
    return name


def test_media_route_is_registered(settings):
    settings.DEBUG = False

    assert reverse("media_file", args=["media_items/test/pic.jpg"]) == (
        "/media/media_items/test/pic.jpg"
    )


@pytest.mark.django_db
def test_media_view_returns_file(client, stored_file):
    response = client.get(reverse("media_file", args=[stored_file]))

    assert response.status_code == 200
    assert response["Content-Type"] == "image/jpeg"
    assert response["Cache-Control"] == "public, max-age=604800, immutable"
    assert response["X-Media-Cache"] == "miss"
    assert response.content == JPEG


@pytest.mark.django_db
def test_media_view_returns_placeholder_for_missing_file(client):
    """Файла нет ни в кэше, ни в хранилище — отдаём заглушку, а не битую картинку."""
    response = client.get(reverse("media_file", args=["nope.jpg"]))

    assert response.status_code == 302
    assert response["X-Media-Placeholder"] == "1"


@pytest.mark.django_db
def test_media_view_rejects_path_traversal(client):
    for path in ("../secret.txt", "a/../../secret.txt", ".env"):
        response = client.get(f"/media/{path}")
        assert response.status_code in (400, 404), path


@pytest.mark.django_db
def test_media_view_rejects_traversal_in_view(rf, db):
    from django.http import Http404

    for path in ("../secret.txt", "a/../../secret.txt", ".hidden"):
        with pytest.raises(Http404):
            media_file(rf.get("/media/x"), path)


@pytest.mark.django_db
def test_leading_slash_stays_inside_media_root(rf, db):
    """Слеш в начале обрезается, выйти за MEDIA_ROOT нельзя — файла просто нет."""
    response = media_file(rf.get("/media/x"), "/etc/passwd")

    assert response.status_code == 302
    assert response["X-Media-Placeholder"] == "1"


@pytest.mark.django_db
def test_media_view_is_get_only(client, stored_file):
    assert client.post(reverse("media_file", args=[stored_file])).status_code == 405


def test_shrink_reduces_large_photo(settings):
    """Большая фотография уменьшается до веб-размера и весит меньше."""
    import io

    from PIL import Image

    from core.imaging import shrink

    settings.MEDIA_SERVE_MAX_SIDE = 1600
    settings.MEDIA_SERVE_QUALITY = 82

    buffer = io.BytesIO()
    Image.new("RGB", (3200, 2400), (120, 140, 200)).save(buffer, format="JPEG", quality=95)
    original = buffer.getvalue()

    result = shrink(original, "photo.jpg")

    with Image.open(io.BytesIO(result)) as image:
        assert max(image.size) <= 1600
    assert len(result) < len(original)


def test_shrink_keeps_small_image(settings):
    """Маленькую картинку не пережимаем — отдаём как есть."""
    import io

    from PIL import Image

    from core.imaging import shrink

    buffer = io.BytesIO()
    Image.new("RGB", (400, 300), (10, 20, 30)).save(buffer, format="JPEG", quality=90)
    original = buffer.getvalue()

    assert shrink(original, "small.jpg") == original


def test_shrink_returns_original_for_broken_file():
    """Битые байты не ломают отдачу — возвращаем исходник."""
    from core.imaging import shrink

    payload = b"not an image at all"

    assert shrink(payload, "broken.jpg") == payload
