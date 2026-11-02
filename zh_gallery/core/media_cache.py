"""Локальный кэш медиафайлов.

Nextcloud может быть недоступен (сеть, обновление, упавший WebDAV) — тогда
картинки должны остаться на сайте. Поэтому каждый отданный файл складывается
в локальный кэш, а команда ``media_cache --warm`` наполняет его заранее.

Работает только для удалённого хранилища: если медиа лежит на локальном диске,
кэш не нужен (``MEDIA_CACHE_ENABLED`` по умолчанию включается для Nextcloud).
"""

from __future__ import annotations

import logging
import shutil
from pathlib import Path

from django.conf import settings

logger = logging.getLogger(__name__)


def is_enabled() -> bool:
    return bool(getattr(settings, "MEDIA_CACHE_ENABLED", False))


def cache_root() -> Path | None:
    """Каталог кэша или None, если кэш выключен."""
    if not is_enabled():
        return None
    root = getattr(settings, "MEDIA_CACHE_ROOT", None)
    return Path(root) if root else None


def cache_path(name: str) -> Path | None:
    """Путь файла в кэше с защитой от выхода за пределы каталога."""
    root = cache_root()
    if root is None:
        return None
    try:
        path = (root / name).resolve()
        path.relative_to(root.resolve())
    except (ValueError, OSError):
        return None
    return path


def read(name: str) -> Path | None:
    """Возвращает путь к закэшированному файлу или None."""
    path = cache_path(name)
    if path is not None and path.is_file() and path.stat().st_size:
        return path
    return None


def store(name: str, payload: bytes) -> Path | None:
    """Кладёт файл в кэш атомарно (через временный файл)."""
    path = cache_path(name)
    if path is None:
        return None
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_name(f"{path.name}.part")
        temporary.write_bytes(payload)
        temporary.replace(path)
    except OSError:
        logger.warning("Не удалось закэшировать %s", name, exc_info=True)
        return None
    return path


def clear() -> int:
    """Полностью очищает кэш, возвращает число удалённых файлов."""
    root = cache_root()
    if root is None or not root.exists():
        return 0
    removed = sum(1 for path in root.rglob("*") if path.is_file())
    shutil.rmtree(root, ignore_errors=True)
    return removed


def stats() -> tuple[int, int]:
    """(количество файлов, суммарный размер в байтах)."""
    root = cache_root()
    if root is None or not root.exists():
        return 0, 0
    files = [path for path in root.rglob("*") if path.is_file()]
    return len(files), sum(path.stat().st_size for path in files)
