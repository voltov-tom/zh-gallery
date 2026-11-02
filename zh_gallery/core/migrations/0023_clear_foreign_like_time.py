"""Сброс «чужих» like_time.

Раньше поле было ``auto_now``, то есть обновлялось при любом ``save()``: главная
показывала «недавно изменённое» вместо «недавно лайкнутого». Здесь обнуляем
like_time у работ, у которых нет ни одного лайка.

Идёт после 0022, где колонка уже стала nullable.
"""

from __future__ import annotations

from django.db import migrations


def clear_foreign_like_time(apps, schema_editor):
    MediaItem = apps.get_model("core", "MediaItem")

    MediaItem.objects.filter(likes__isnull=True).update(like_time=None)


def noop(apps, schema_editor):
    """Обратной операции нет: исходное значение было ошибкой."""


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0022_schema_updates"),
    ]

    operations = [
        migrations.RunPython(clear_foreign_like_time, noop),
    ]
