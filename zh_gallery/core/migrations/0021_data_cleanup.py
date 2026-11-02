"""Нормализация данных перед ужесточением схемы.

Нужна, чтобы миграция 0022 не упала на живой базе:

* текстовые поля становятся ``NOT NULL DEFAULT ''`` — сначала заменяем NULL;
* ``views`` становится ``PositiveIntegerField`` — отрицательные значения (следы
  ручных правок в админке) обнуляем.

Сброс ``like_time`` вынесен в 0023: колонка становится nullable только в 0022,
а до этого ``NOT NULL`` (её задал ``auto_now=True`` в старых миграциях).
"""

from __future__ import annotations

from django.db import migrations


def normalize_null_text_fields(apps, schema_editor):
    About = apps.get_model("core", "About")
    SubCategory = apps.get_model("core", "SubCategory")
    MediaItem = apps.get_model("core", "MediaItem")
    MediaItemReview = apps.get_model("core", "MediaItemReview")

    About.objects.filter(body__isnull=True).update(body="")
    SubCategory.objects.filter(description__isnull=True).update(description="")
    MediaItem.objects.filter(description__isnull=True).update(description="")
    MediaItemReview.objects.filter(content__isnull=True).update(content="")

    MediaItem.objects.filter(views__lt=0).update(views=0)


def noop(apps, schema_editor):
    """Откат не восстанавливает NULL: данные нормализованы в одну сторону."""


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0020_alter_about_options_maincategory_title_en_and_more"),
    ]

    operations = [
        migrations.RunPython(normalize_null_text_fields, noop),
    ]
