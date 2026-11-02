"""Тесты хранилища Nextcloud и WebDAV-клиента (без сети)."""

from __future__ import annotations

import pytest
from django.core.files.base import ContentFile

from core.integrations.nextcloud import NextcloudError, NextcloudWebDAVClient
from core.storage import NextcloudStorage


class StubResponse:
    def __init__(self, status_code: int = 200, content: bytes = b"", headers=None):
        self.status_code = status_code
        self.content = content
        self.headers = headers or {}


class StubSession:
    """Подменяет requests.Session и записывает вызовы."""

    def __init__(self, responses=None):
        self.responses = list(responses or [])
        self.calls: list[tuple[str, str, dict]] = []

    def request(self, method, url, **kwargs):
        self.calls.append((method, url, kwargs))
        if self.responses:
            return self.responses.pop(0)
        return StubResponse(200)


class FakeNextcloudClient:
    def __init__(self, fail: bool = False):
        self.files: dict[str, bytes] = {}
        self.deleted: list[str] = []
        self.fail = fail

    def upload(self, name, payload):
        if self.fail:
            raise NextcloudError("boom")
        self.files[name] = payload

    def download(self, name):
        if self.fail or name not in self.files:
            raise NextcloudError("нет файла")
        return self.files[name]

    def exists(self, name):
        return name in self.files

    def size(self, name):
        return len(self.files.get(name, b""))

    def delete(self, name):
        if self.fail:
            raise NextcloudError("boom")
        self.deleted.append(name)
        self.files.pop(name, None)


# ---------------------------------------------------------------------------
# WebDAV-клиент
# ---------------------------------------------------------------------------
def test_endpoint_includes_login_root_and_quotes_path():
    client = NextcloudWebDAVClient(
        hostname="https://cloud.example/", login="user", password="pw", root="gallery"
    )

    url = client.endpoint("media item/фото 1.jpg")

    assert url.startswith("https://cloud.example/remote.php/dav/files/user/gallery/")
    assert "%D1%84" in url  # кириллица закодирована
    assert " " not in url


def test_upload_creates_directories_then_puts_file():
    session = StubSession([StubResponse(201), StubResponse(405), StubResponse(201)])
    client = NextcloudWebDAVClient(
        hostname="https://cloud.example",
        login="user",
        password="pw",
        root="gallery",
        session=session,
    )

    client.upload("2024/05/pic.jpg", b"data")

    methods = [call[0] for call in session.calls]
    assert methods == ["MKCOL", "MKCOL", "PUT"]
    assert session.calls[-1][2]["data"] == b"data"


def test_upload_raises_on_error_status():
    session = StubSession([StubResponse(500)])
    client = NextcloudWebDAVClient(
        hostname="https://cloud.example", login="user", password="pw", session=session
    )

    with pytest.raises(NextcloudError):
        client.upload("pic.jpg", b"data")


def test_exists_and_size_use_head():
    session = StubSession([StubResponse(200), StubResponse(200, headers={"Content-Length": "42"})])
    client = NextcloudWebDAVClient(
        hostname="https://cloud.example", login="user", password="pw", session=session
    )

    assert client.exists("pic.jpg") is True
    assert client.size("pic.jpg") == 42
    assert [call[0] for call in session.calls] == ["HEAD", "HEAD"]


def test_exists_returns_false_for_404():
    session = StubSession([StubResponse(404)])
    client = NextcloudWebDAVClient(
        hostname="https://cloud.example", login="user", password="pw", session=session
    )

    assert client.exists("missing.jpg") is False


def test_delete_ignores_missing_file():
    session = StubSession([StubResponse(404)])
    client = NextcloudWebDAVClient(
        hostname="https://cloud.example", login="user", password="pw", session=session
    )

    client.delete("missing.jpg")  # не должно бросать


def test_download_raises_for_missing_file():
    session = StubSession([StubResponse(404)])
    client = NextcloudWebDAVClient(
        hostname="https://cloud.example", login="user", password="pw", session=session
    )

    with pytest.raises(NextcloudError):
        client.download("missing.jpg")


def test_client_requires_credentials():
    with pytest.raises(NextcloudError):
        NextcloudWebDAVClient(hostname="", login="user", password="pw")


# ---------------------------------------------------------------------------
# Django-хранилище
# ---------------------------------------------------------------------------
def test_storage_saves_and_reads_via_client():
    fake = FakeNextcloudClient()
    storage = NextcloudStorage(client=fake)

    saved_name = storage.save("media_items/pic.jpg", ContentFile(b"binary"))

    assert saved_name == "media_items/pic.jpg"
    assert storage.exists("media_items/pic.jpg")
    assert storage.size("media_items/pic.jpg") == 6
    with storage.open("media_items/pic.jpg") as handle:
        assert handle.read() == b"binary"


def test_storage_delete_removes_file():
    fake = FakeNextcloudClient()
    fake.files["pic.jpg"] = b"data"
    storage = NextcloudStorage(client=fake)

    storage.delete("pic.jpg")

    assert fake.deleted == ["pic.jpg"]
    assert not storage.exists("pic.jpg")


def test_storage_raises_io_error_when_upload_fails():
    storage = NextcloudStorage(client=FakeNextcloudClient(fail=True))

    with pytest.raises(IOError):
        storage.save("pic.jpg", ContentFile(b"data"))


def test_storage_open_raises_file_not_found():
    storage = NextcloudStorage(client=FakeNextcloudClient())

    with pytest.raises(FileNotFoundError):
        storage.open("missing.jpg")


def test_storage_url_uses_media_url_by_default(settings):
    settings.MEDIA_URL = "/media/"
    settings.NEXTCLOUD_PUBLIC_URL = ""
    storage = NextcloudStorage(client=FakeNextcloudClient())

    assert storage.url("a/b.jpg") == "/media/a/b.jpg"


def test_storage_url_prefers_public_url(settings):
    settings.NEXTCLOUD_PUBLIC_URL = "https://cloud.example/s/abc/download"
    storage = NextcloudStorage(client=FakeNextcloudClient())

    assert storage.url("b.jpg") == "https://cloud.example/s/abc/download/b.jpg"
