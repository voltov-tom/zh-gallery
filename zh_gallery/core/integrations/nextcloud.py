"""Клиент Nextcloud по WebDAV — только то, что нужно хранилищу.

Раньше проект использовал пакет ``webdavclient3`` (последний релиз — 2021 год),
который тянет устаревшие зависимости, а его клиент ходил в сеть прямо из
конструктора. Здесь минимум на ``requests``: PUT / GET / HEAD / DELETE / MKCOL.
"""

from __future__ import annotations

import logging
import posixpath
import re
from urllib.parse import quote, unquote

import requests

logger = logging.getLogger("core.integrations.nextcloud")


class NextcloudError(RuntimeError):
    """Любая проблема обмена с Nextcloud."""


class NextcloudWebDAVClient:
    """Тонкая обёртка над WebDAV-эндпоинтом Nextcloud."""

    def __init__(
        self,
        hostname: str,
        login: str,
        password: str,
        root: str = "",
        timeout: int = 30,
        session: requests.Session | None = None,
        base_url: str = "",
    ) -> None:
        if not (base_url or hostname) or not login or not password:
            raise NextcloudError(
                "Не заданы NEXTCLOUD_HOSTNAME / NEXTCLOUD_LOGIN / NEXTCLOUD_PASSWORD"
            )
        self.hostname = hostname.rstrip("/")
        self.login = login
        self.password = password
        self.root = root.strip("/")
        self.timeout = timeout
        self._session = session or requests.Session()
        self.base_url = self.build_base_url(base_url or self.hostname)

    def build_base_url(self, hostname: str) -> str:
        """Адрес WebDAV-корня, к которому просто дописывается путь файла.

        Nextcloud отдаёт файлы по ``/remote.php/dav/files/<user>/``, но в
        конфигурации проекта исторически записан полный адрес
        (``WEBDAV_HOSTNAME`` = ``https://host/remote.php/dav/files/user/``).
        Поэтому если путь уже содержит ``remote.php``, используем его как есть
        и не подставляем логин — это и есть поведение старого клиента.
        """
        hostname = hostname.rstrip("/")
        if "remote.php" in hostname:
            return f"{hostname}/"
        return f"{hostname}/remote.php/dav/files/{quote(self.login)}/"

    @classmethod
    def from_settings(cls) -> NextcloudWebDAVClient:
        from django.conf import settings

        return cls(
            hostname=settings.NEXTCLOUD_HOSTNAME,
            login=settings.NEXTCLOUD_LOGIN,
            password=settings.NEXTCLOUD_PASSWORD,
            root=settings.NEXTCLOUD_ROOT,
            timeout=settings.NEXTCLOUD_TIMEOUT,
            base_url=getattr(settings, "NEXTCLOUD_BASE_URL", ""),
        )

    # ------------------------------------------------------------------
    # внутреннее
    # ------------------------------------------------------------------
    def endpoint(self, name: str = "") -> str:
        """Полный URL файла внутри WebDAV-дерева пользователя."""
        segments: list[str] = []
        for chunk in (self.root, name.strip("/")):
            if chunk:
                # «..» и «.» не пропускаем: иначе имя файла уводит за пределы root
                segments.extend(
                    part for part in chunk.split("/") if part and part not in (".", "..")
                )
        if not segments:
            return self.base_url
        return self.base_url + "/".join(quote(part) for part in segments)

    def _request(self, method: str, name: str = "", **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        kwargs.setdefault("auth", (self.login, self.password))
        try:
            return self._session.request(method, self.endpoint(name), **kwargs)
        except requests.RequestException as exc:  # сеть/таймаут/DNS
            raise NextcloudError(f"WebDAV {method} {name}: {exc}") from exc

    # ------------------------------------------------------------------
    # операции
    # ------------------------------------------------------------------
    def upload(self, name: str, payload: bytes) -> None:
        """Загружает файл, при необходимости создавая родительские папки."""
        directory = posixpath.dirname(name.strip("/"))
        if directory:
            self.mkdirs(directory)

        response = self._request("PUT", name, data=payload)
        if response.status_code not in (200, 201, 204):
            raise NextcloudError(f"Не удалось загрузить {name}: HTTP {response.status_code}")
        logger.debug("Файл загружен в Nextcloud: %s", name)

    def download(self, name: str) -> bytes:
        response = self._request("GET", name)
        if response.status_code == 404:
            raise NextcloudError(f"Файл не найден в Nextcloud: {name}")
        if response.status_code != 200:
            raise NextcloudError(f"Не удалось скачать {name}: HTTP {response.status_code}")
        return response.content

    def exists(self, name: str) -> bool:
        response = self._request("HEAD", name)
        if response.status_code == 200:
            return True
        if response.status_code == 404:
            return False
        logger.warning("WebDAV HEAD %s вернул HTTP %s", name, response.status_code)
        return False

    def size(self, name: str) -> int | None:
        response = self._request("HEAD", name)
        if response.status_code != 200:
            return None
        length = response.headers.get("Content-Length")
        return int(length) if length and length.isdigit() else None

    def move(self, source: str, destination: str) -> None:
        """Перемещает файл (WebDAV MOVE) — без скачивания и повторной загрузки."""
        directory = posixpath.dirname(destination.strip("/"))
        if directory:
            self.mkdirs(directory)

        response = self._request(
            "MOVE",
            source,
            headers={"Destination": self.endpoint(destination), "Overwrite": "F"},
        )
        if response.status_code not in (201, 204):
            raise NextcloudError(
                f"Не удалось переместить {source} -> {destination}: HTTP {response.status_code}"
            )

    def delete(self, name: str) -> None:
        """Удаляет файл. Отсутствие файла ошибкой не считается."""
        response = self._request("DELETE", name)
        if response.status_code not in (200, 204, 404):
            raise NextcloudError(f"Не удалось удалить {name}: HTTP {response.status_code}")

    def mkdirs(self, directory: str) -> None:
        """Создаёт папку вместе со всеми родителями (MKCOL идемпотентен)."""
        directory = directory.strip("/")
        if not directory:
            return
        parts = directory.split("/")
        for depth in range(1, len(parts) + 1):
            current = "/".join(parts[:depth])
            response = self._request("MKCOL", current)
            # 201 — создали, 405 — уже существует, 301/409 — родитель есть
            if response.status_code not in (200, 201, 405, 301, 409):
                raise NextcloudError(
                    f"Не удалось создать папку {current}: HTTP {response.status_code}"
                )

    def list_files(self, directory: str = "") -> list[str]:
        """Имена файлов внутри папки (без самой папки и без подпапок)."""
        body = (
            '<?xml version="1.0"?>'
            '<d:propfind xmlns:d="DAV:"><d:prop><d:resourcetype/></d:prop></d:propfind>'
        )
        response = self._request("PROPFIND", directory, data=body, headers={"Depth": "1"})
        if response.status_code not in (200, 207):
            raise NextcloudError(
                f"Не удалось получить список {directory}: HTTP {response.status_code}"
            )

        names: list[str] = []
        for href in re.findall(r"<d:href>([^<]+)</d:href>", response.text):
            path = unquote(href).rstrip("/")
            name = path.split("/")[-1]
            if not name or name in names:
                continue
            names.append(name)

        # первым в ответе всегда идёт сама папка — убираем её
        own_name = posixpath.basename(directory.rstrip("/"))
        return [name for name in names if name != own_name]
