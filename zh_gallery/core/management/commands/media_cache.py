"""Прогрев локального кэша медиа.

Nextcloud может быть недоступен — кэш позволяет показывать уже отданные
картинки. Команда наполняет его заранее::

    python manage.py media_cache            # скачать все файлы из БД в кэш
    python manage.py media_cache --limit 10
    python manage.py media_cache --clear    # очистить кэш

После прогрева сайт переживает падение WebDAV: картинки отдаются с диска.
"""

from __future__ import annotations

from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand

from core import media_cache
from core.selectors import all_image_names


class Command(BaseCommand):
    help = "Наполняет локальный кэш медиафайлов (или очищает его)"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Очистить кэш")
        parser.add_argument("--limit", type=int, default=0, help="Обработать только N файлов")

    def handle(self, *args, **options):
        if not media_cache.is_enabled():
            self.stderr.write(
                self.style.ERROR(
                    "Кэш медиа выключен (MEDIA_CACHE_ENABLED=False) — "
                    "включать есть смысл только для удалённого хранилища."
                )
            )
            return

        if options["clear"]:
            removed = media_cache.clear()
            self.stdout.write(self.style.SUCCESS(f"Кэш очищен, удалено файлов: {removed}"))
            return

        names = list(all_image_names())
        if options["limit"]:
            names = names[: options["limit"]]

        cached_now = 0
        added = 0
        missing: list[str] = []

        for name in names:
            if media_cache.read(name) is not None:
                cached_now += 1
                continue
            try:
                with default_storage.open(name, "rb") as handle:
                    payload = handle.read()
            except (FileNotFoundError, OSError):
                missing.append(name)
                continue
            if media_cache.store(name, payload) is not None:
                added += 1

        files, size = media_cache.stats()
        self.stdout.write(f"Обработано записей: {len(names)}")
        self.stdout.write(f"Уже было в кэше: {cached_now}, добавлено: {added}")
        self.stdout.write(f"В кэше сейчас: {files} файлов, {size / 1024 / 1024:.1f} МБ")

        for name in missing[:10]:
            self.stdout.write(self.style.WARNING(f"  нет в хранилище: {name}"))

        if missing:
            self.stderr.write(self.style.ERROR(f"Недоступных файлов: {len(missing)}"))
            return

        self.stdout.write(self.style.SUCCESS("Кэш готов"))
