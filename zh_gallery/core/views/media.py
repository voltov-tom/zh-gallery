"""Отдача медиафайлов через приложение.

Нужно для режима ``MEDIA_STORAGE=nextcloud``: файлы лежат в WebDAV, локального
каталога с ними нет, поэтому nginx не может отдать их алиасом. Тогда nginx
проксирует ``/media/`` в Django, а эта вьюха стримит файл из хранилища.

Порядок источников:

1. локальный кэш (``core/media_cache.py``) — работает, даже если WebDAV упал;
2. хранилище (диск или Nextcloud) — удачный ответ сразу попадает в кэш;
3. заглушка ``core/images/no_photo.jpeg``, если файла нет нигде.
"""

from __future__ import annotations

import logging
from pathlib import Path

from django.core.files.storage import default_storage
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import redirect
from django.templatetags.static import static
from django.utils.http import content_disposition_header
from django.views.decorators.http import require_safe

from core import imaging, media_cache

logger = logging.getLogger(__name__)

PLACEHOLDER_STATIC_PATH = "core/images/no_photo.jpeg"

# Отдаём как картинки только эти расширения. Всё остальное — вложением:
# иначе случайно попавший в хранилище .html/.svg исполнится на нашем домене.
IMAGE_CONTENT_TYPES = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".webp": "image/webp",
    ".gif": "image/gif",
    ".avif": "image/avif",
}


def _clean_path(path: str) -> str:
    """Не пускаем «..», пустые сегменты и скрытые файлы."""
    path = (path or "").strip("/")
    segments = path.split("/")
    if not path or any(
        segment in ("", ".", "..") or segment.startswith(".") for segment in segments
    ):
        raise Http404("Некорректный путь к файлу")
    return path


def _content_type(name: str) -> str:
    return IMAGE_CONTENT_TYPES.get(Path(name).suffix.lower(), "application/octet-stream")


def _is_image(name: str) -> bool:
    return Path(name).suffix.lower() in IMAGE_CONTENT_TYPES


def _set_media_headers(response, name: str, variant: str) -> None:
    response["Cache-Control"] = "public, max-age=604800, immutable"
    response["X-Media-Variant"] = variant
    response["Content-Disposition"] = content_disposition_header(
        as_attachment=not _is_image(name), filename=Path(name).name
    )


def _cached_response(path: Path, name: str, variant: str = "web") -> FileResponse:
    response = FileResponse(path.open("rb"), content_type=_content_type(name))
    _set_media_headers(response, name, variant)
    response["X-Media-Cache"] = "hit"
    return response


def _bytes_response(payload: bytes, name: str, variant: str = "web") -> HttpResponse:
    response = HttpResponse(payload, content_type=_content_type(name))
    _set_media_headers(response, name, variant)
    response["X-Media-Cache"] = "miss"
    return response


def _placeholder_response():
    """Файла нет ни в кэше, ни в хранилище — показываем заглушку."""
    response = redirect(static(PLACEHOLDER_STATIC_PATH))
    # 302 не кэшируем: как только файл появится, отдадим настоящую картинку
    response["Cache-Control"] = "no-store"
    response["X-Media-Placeholder"] = "1"
    return response


@require_safe
def media_file(request, path: str):
    """Отдаёт файл из кэша или из default_storage (диск / Nextcloud).

    По умолчанию — лёгкая версия для карточек. С ``?original=1`` отдаётся
    оригинал (страница работы): он тоже кэшируется, но отдельным вариантом.
    """
    name = _clean_path(path)
    original = request.GET.get("original") in {"1", "true", "yes"}
    variant = "orig" if original else "web"

    cached = media_cache.read(name, variant)
    if cached is not None:
        return _cached_response(cached, name, variant)

    try:
        stored = default_storage.open(name, "rb")
        try:
            payload = stored.read()
        finally:
            stored.close()
    except (FileNotFoundError, OSError) as exc:
        logger.warning("Медиафайл %s недоступен: %s", name, exc)
        return _placeholder_response()

    if not payload:
        logger.warning("Медиафайл %s пустой — отдаём заглушку", name)
        return _placeholder_response()

    if not original:
        # в кэш и в ответ кладём «веб-размер», а не оригинал с камеры
        payload = imaging.shrink(payload, name)

    media_cache.store(name, payload, variant)
    return _bytes_response(payload, name, variant)
