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
    assert response["Cache-Control"] == "public, max-age=604800"
    assert b"".join(response.streaming_content) == JPEG


@pytest.mark.django_db
def test_media_view_404_for_missing_file(client):
    response = client.get(reverse("media_file", args=["nope.jpg"]))

    assert response.status_code == 404


@pytest.mark.django_db
def test_media_view_rejects_path_traversal(client):
    for path in ("../secret.txt", "a/../../secret.txt", ".env"):
        response = client.get(f"/media/{path}")
        assert response.status_code in (400, 404), path


@pytest.mark.django_db
def test_media_view_rejects_traversal_in_view(rf, db):
    from django.http import Http404

    for path in ("../secret.txt", "a/../../secret.txt", "/etc/passwd", ".hidden"):
        with pytest.raises(Http404):
            media_file(rf.get("/media/x"), path)


@pytest.mark.django_db
def test_media_view_is_get_only(client, stored_file):
    assert client.post(reverse("media_file", args=[stored_file])).status_code == 405
