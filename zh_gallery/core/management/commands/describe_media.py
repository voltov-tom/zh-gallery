"""Генерация описаний работ через vision-модель.

Примеры:

    python manage.py describe_media --pk 16            # одна работа
    python manage.py describe_media --missing          # все без описания
    python manage.py describe_media --missing --dry-run  # только показать
"""

from __future__ import annotations

from django.core.management.base import BaseCommand, CommandError
from django.db.models import Q

from core.integrations.ai import AIDescriptionError, request_description
from core.models import MediaItem
from core.services import generate_media_description


class Command(BaseCommand):
    help = "Сгенерировать описания работ через ИИ"

    def add_arguments(self, parser):
        parser.add_argument("--pk", type=int, action="append", help="ID работы (можно несколько)")
        parser.add_argument(
            "--missing", action="store_true", help="только работы без русского описания"
        )
        parser.add_argument("--limit", type=int, default=0, help="максимум работ за прогон")
        parser.add_argument(
            "--dry-run", action="store_true", help="показать результат, ничего не сохраняя"
        )

    def handle(self, *args, **options):
        queryset = MediaItem.objects.order_by("pk")
        if options["pk"]:
            queryset = queryset.filter(pk__in=options["pk"])
        elif options["missing"]:
            queryset = queryset.filter(Q(description_ru="") | Q(description_ru__isnull=True))
        elif not options["pk"]:
            raise CommandError("укажите --pk или --missing")

        if options["limit"]:
            queryset = queryset[: options["limit"]]

        done = failed = 0
        for media_item in queryset:
            try:
                if options["dry_run"]:
                    texts = request_description(media_item)
                else:
                    texts = generate_media_description(media_item)
            except AIDescriptionError as error:
                failed += 1
                self.stderr.write(f"✗ {media_item.pk} {media_item.title}: {error}")
                continue

            done += 1
            prefix = "·" if options["dry_run"] else "✓"
            self.stdout.write(f"{prefix} {media_item.pk} {media_item.title}: {texts['ru']}")

        self.stdout.write(self.style.SUCCESS(f"готово: {done}, ошибок: {failed}"))
