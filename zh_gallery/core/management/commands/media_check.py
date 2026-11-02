"""Проверка связки БД ↔ хранилище медиа.

Примеры::

    python manage.py media_check                # подключение + сводка
    python manage.py media_check --download     # ещё и скачать файлы
    python manage.py media_check --limit 5      # только первые 5 записей

Полезно после переезда на Nextcloud: сразу видно, какие файлы из БД в хранилище
отсутствуют.
"""

from __future__ import annotations

import contextlib

from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from core.selectors import all_image_names


def is_image(payload: bytes) -> bool:
    return payload[:2] == b"\xff\xd8" or payload[:8] == b"\x89PNG\r\n\x1a\n"


class Command(BaseCommand):
    help = "Проверяет, что файлы из БД доступны в хранилище (локально или в Nextcloud)"

    def add_arguments(self, parser):
        parser.add_argument("--limit", type=int, default=0, help="Проверить только N файлов")
        parser.add_argument(
            "--download", action="store_true", help="Скачать файлы и проверить формат"
        )

    def handle(self, *args, **options):
        storage = default_storage
        names = list(all_image_names())
        if options["limit"]:
            names = names[: options["limit"]]

        self.stdout.write(f"Хранилище: {storage.__class__.__module__}.{storage.__class__.__name__}")
        if hasattr(storage, "base_url"):
            self.stdout.write(f"Базовый URL WebDAV: {storage.base_url}")
        self.stdout.write(f"Файлов в БД: {len(names)}")

        missing: list[str] = []
        broken: list[str] = []
        total_bytes = 0

        for name in names:
            if not storage.exists(name):
                missing.append(name)
                continue
            # размер не критичен: Nextcloud может не отдать Content-Length
            with contextlib.suppress(Exception):
                total_bytes += storage.size(name) or 0
            if options["download"]:
                try:
                    with storage.open(name, "rb") as handle:
                        if not is_image(handle.read(16)):
                            broken.append(name)
                except Exception:  # noqa: BLE001
                    broken.append(name)

        self.stdout.write(f"Найдено: {len(names) - len(missing)}, отсутствует: {len(missing)}")
        self.stdout.write(f"Суммарный размер: {total_bytes / 1024 / 1024:.1f} МБ")

        for name in missing[:10]:
            self.stdout.write(self.style.WARNING(f"  нет файла: {name}"))
        for name in broken[:10]:
            self.stdout.write(self.style.ERROR(f"  не картинка: {name}"))

        if missing or broken:
            self.stderr.write(self.style.ERROR(f"Проблемных файлов: {len(missing) + len(broken)}"))
            return

        self.stdout.write(self.style.SUCCESS("Все файлы на месте"))
