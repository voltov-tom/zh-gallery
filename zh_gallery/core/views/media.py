"""Отдача медиафайлов через приложение.

Нужно для режима ``MEDIA_STORAGE=nextcloud``: файлы лежат в WebDAV, локального
каталога с ними нет, поэтому nginx не может отдать их алиасом. Тогда nginx
проксирует ``/media/`` в Django, а эта вьюха стримит файл из хранилища.

Для локального диска тот же маршрут работает как fallback (в проде его
перекрывает ``location /media/ { alias ...; }`` в nginx).
"""

from __future__ import annotations

import mimetypes

from django.core.files.storage import default_storage
from django.http import FileResponse, Http404
from django.views.decorators.http import require_GET


def _clean_path(path: str) -> str:
    """Не пускаем «..», пустые сегменты и скрытые файлы."""
    path = (path or "").strip("/")
    segments = path.split("/")
    if not path or any(
        segment in ("", ".", "..") or segment.startswith(".") for segment in segments
    ):
        raise Http404("Некорректный путь к файлу")
    return path


@require_GET
def media_file(request, path: str):
    """Отдаёт файл из default_storage (диск или Nextcloud)."""
    name = _clean_path(path)

    try:
        stored_file = default_storage.open(name, "rb")
    except (FileNotFoundError, OSError) as exc:
        raise Http404(f"Файл {name} не найден") from exc

    content_type = mimetypes.guess_type(name)[0] or "application/octet-stream"
    response = FileResponse(stored_file, content_type=content_type)
    # Файлы галереи не меняются: агрессивный кэш и корректное имя
    response["Cache-Control"] = "public, max-age=604800"
    return response
