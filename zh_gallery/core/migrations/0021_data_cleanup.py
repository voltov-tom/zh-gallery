"""Нормализация данных перед ужесточением схемы.

Нужна, чтобы миграция 0022 не упала на живой базе:

* текстовые поля становятся ``NOT NULL DEFAULT ''`` — сначала заменяем NULL;
* ``views`` становится ``PositiveIntegerField`` — отрицательные значения (следы
  ручных правок в админке) обнуляем;
* ``like_time`` раньше был ``auto_now``, то есть содержал время последнего
  сохранения. Обнуляем его там, где лайков нет, чтобы главная снова показывала
  «недавно лайкнутое», а не «недавно изменённое».
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


def clear_foreign_like_time(apps, schema_editor):
    MediaItem = apps.get_model("core", "MediaItem")

    # like_time, проставленный не лайком, а обычным save() — сбрасываем
    MediaItem.objects.filter(likes__isnull=True).update(like_time=None)


def noop(apps, schema_editor):
    """Откат не восстанавливает NULL: данные нормализованы в одну сторону."""


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0020_alter_about_options_maincategory_title_en_and_more"),
    ]

    operations = [
        migrations.RunPython(normalize_null_text_fields, noop),
        migrations.RunPython(clear_foreign_like_time, noop),
    ]
