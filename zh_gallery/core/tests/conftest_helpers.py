"""Хелперы, доступные тестам без импорта conftest."""

from __future__ import annotations

import io

from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image


def make_image_file(name: str = "test.jpg", color: tuple[int, int, int] = (120, 140, 160)):
    buffer = io.BytesIO()
    Image.new("RGB", (16, 12), color).save(buffer, format="JPEG")
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/jpeg")
