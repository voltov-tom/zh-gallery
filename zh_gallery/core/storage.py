"""Хранилище медиа: локальный диск (по умолчанию) или Nextcloud WebDAV.

Выбор задаётся переменной ``MEDIA_STORAGE=local|nextcloud`` — см. settings/base.py.

Класс ленивый: соединение с Nextcloud открывается только при первом обращении
к файлу, поэтому ``manage.py check``, ``migrate`` и тесты работают без сети.
"""

from __future__ import annotations

import posixpath

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

from .integrations.nextcloud import NextcloudError, NextcloudWebDAVClient


@deconstructible
class NextcloudStorage(Storage):
    """Django-хранилище поверх Nextcloud WebDAV."""

    def __init__(self, client: NextcloudWebDAVClient | None = None) -> None:
        self._client = client

    @property
    def client(self) -> NextcloudWebDAVClient:
        if self._client is None:
            self._client = NextcloudWebDAVClient.from_settings()
        return self._client

    # ------------------------------------------------------------------
    # Storage API
    # ------------------------------------------------------------------
    def _open(self, name: str, mode: str = "rb"):
        try:
            payload = self.client.download(name)
        except NextcloudError as exc:
            raise FileNotFoundError(f"Файл {name} недоступен в Nextcloud") from exc
        return ContentFile(payload, name=name)

    def _save(self, name: str, content) -> str:
        content.seek(0)
        try:
            self.client.upload(name, content.read())
        except NextcloudError as exc:
            raise OSError(f"Не удалось сохранить {name} в Nextcloud") from exc
        return name

    def delete(self, name: str) -> None:
        try:
            self.client.delete(name)
        except NextcloudError as exc:
            raise OSError(f"Не удалось удалить {name} из Nextcloud") from exc

    def exists(self, name: str) -> bool:
        try:
            return self.client.exists(name)
        except NextcloudError:
            return False

    def size(self, name: str) -> int:
        try:
            return self.client.size(name) or 0
        except NextcloudError:
            return 0

    def url(self, name: str) -> str:
        """Публичная ссылка.

        Файлы лежат в Nextcloud, поэтому по умолчанию используется MEDIA_URL —
        его должен отдавать nginx (алиас на смонтированную папку) или публичная
        ссылка Nextcloud, если задан NEXTCLOUD_PUBLIC_URL.
        """
        base = settings.NEXTCLOUD_PUBLIC_URL or settings.MEDIA_URL
        return f"{base.rstrip('/')}/{name.lstrip('/')}"

    def get_valid_name(self, name: str) -> str:
        return super().get_valid_name(posixpath.basename(name))
