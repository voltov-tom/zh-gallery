"""Тесты команды media_check."""

from __future__ import annotations

import pytest
from django.core.management import call_command

from core.models import MediaItem


@pytest.mark.django_db
def test_media_check_reports_all_files_present(media_item, capsys):
    call_command("media_check", "--download", verbosity=0)

    out = capsys.readouterr().out
    assert "Все файлы на месте" in out
    assert "Файлов в БД: 1" in out


@pytest.mark.django_db
def test_media_check_detects_missing_file(media_item, capsys):
    media_item.image.storage.delete(media_item.image.name)

    call_command("media_check", verbosity=0)

    captured = capsys.readouterr()
    assert "отсутствует: 1" in captured.out
    assert "Проблемных файлов: 1" in captured.err


@pytest.mark.django_db
def test_media_check_limit(media_item, subcategory, capsys):
    second = MediaItem(subcategory=subcategory, title="Второй")
    second.image.save("second.jpg", media_item.image, save=True)

    call_command("media_check", "--limit", "1", verbosity=0)

    assert "Файлов в БД: 1" in capsys.readouterr().out
