"""Раскладывает уже загруженные работы по папкам подкатегорий.

Старые работы лежат в корне хранилища (``<uuid>.jpeg``), новые загружаются в
``<slug подкатегории>/<имя>.jpg``. Команда переносит существующие файлы в новую
структуру и обновляет пути в базе.

Примеры:

    python manage.py reorganize_media --dry-run     # только показать план
    python manage.py reorganize_media               # перенести
    python manage.py reorganize_media --adopt       # файл уже перенесён, обновить только БД
"""

from __future__ import annotations

from pathlib import Path

from django.core.management.base import BaseCommand
from slugify import slugify

from core.models import MediaItem


def target_name(media_item: MediaItem) -> str:
    """Куда должен лежать файл: ``<категория>/<подкатегория>/<имя>``."""
    folder = "bez-kategorii"
    if media_item.subcategory_id:
        subcategory = media_item.subcategory
        folder = f"{subcategory.category.slug}/{subcategory.slug}"

    stem = slugify(Path(media_item.image.name).stem)[:60] or "image"
    suffix = Path(media_item.image.name).suffix.lower() or ".jpg"
    return f"{folder}/{stem}{suffix}"


class Command(BaseCommand):
    help = "Перенести существующие файлы работ в папки подкатегорий"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", action="store_true", help="показать план, ничего не менять"
        )
        parser.add_argument(
            "--adopt",
            action="store_true",
            help="файлы уже перенесены — обновить только пути в базе",
        )
        parser.add_argument("--limit", type=int, default=0, help="максимум работ за прогон")

    def handle(self, *args, **options):
        dry_run = options["dry_run"]
        adopt = options["adopt"]

        storage = MediaItem._meta.get_field("image").storage
        queryset = MediaItem.objects.exclude(image="").select_related("subcategory").order_by("pk")
        if options["limit"]:
            queryset = queryset[: options["limit"]]

        moved = skipped = failed = 0
        for media_item in queryset:
            current = media_item.image.name
            folder = ""
            if media_item.subcategory_id:
                subcategory = media_item.subcategory
                folder = f"{subcategory.category.slug}/{subcategory.slug}/"
            if folder and current.startswith(folder):
                skipped += 1
                continue

            new_name = target_name(media_item)
            if current == new_name:
                skipped += 1
                continue

            source_exists = storage.exists(current)
            # имя занято, а исходник ещё на месте — добавляем числовой суффикс
            if source_exists:
                counter = 2
                while storage.exists(new_name):
                    stem, dot, suffix = new_name.rpartition(".")
                    new_name = f"{stem}-{counter}.{suffix}" if dot else f"{new_name}-{counter}"
                    counter += 1

            self.stdout.write(f"{media_item.pk} {media_item.title}: {current} -> {new_name}")

            if dry_run:
                moved += 1
                continue

            try:
                if source_exists:
                    if hasattr(storage, "client"):
                        storage.client.move(current, new_name)
                    else:
                        # локальное хранилище: переносим через чтение/запись
                        with storage.open(current, "rb") as source:
                            storage.save(new_name, source)
                        storage.delete(current)
                elif not adopt:
                    raise FileNotFoundError(
                        f"файла нет ни по старому, ни по новому пути: {current}"
                    )
            except Exception as error:  # noqa: BLE001 — показываем причину и идём дальше
                failed += 1
                self.stderr.write(f"  ✗ не удалось: {error}")
                continue

            media_item.image.name = new_name
            media_item.save(update_fields=["image"])
            moved += 1

        prefix = "[dry-run] " if dry_run else ""
        self.stdout.write(
            self.style.SUCCESS(
                f"{prefix}перенесено: {moved}, пропущено: {skipped}, ошибок: {failed}"
            )
        )
