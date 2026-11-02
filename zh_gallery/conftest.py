"""Общие фикстуры для всех тестов проекта."""

from __future__ import annotations

import io

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image

from core.models import About, MainCategory, MediaItem, MediaItemReview, SubCategory


def make_image_file(name: str = "test.jpg", color: tuple[int, int, int] = (200, 120, 150)):
    """Валидный JPEG в памяти — ImageField не примет мусор."""
    buffer = io.BytesIO()
    Image.new("RGB", (16, 12), color).save(buffer, format="JPEG")
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/jpeg")


@pytest.fixture
def image_file():
    return make_image_file


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(
        username="tester",
        email="tester@example.com",
        password="secret-12345",
    )


@pytest.fixture
def other_user(db):
    return get_user_model().objects.create_user(
        username="another",
        email="another@example.com",
        password="secret-12345",
    )


@pytest.fixture
def admin_user(db):
    return get_user_model().objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="secret-12345",
    )


@pytest.fixture
def category(db):
    return MainCategory.objects.create(title="Живопись")


@pytest.fixture
def subcategory(db, category):
    return SubCategory.objects.create(category=category, title="Портреты")


@pytest.fixture
def media_item(db, subcategory):
    item = MediaItem(subcategory=subcategory, title="Тихий взгляд", description="описание")
    item.image.save("test.jpg", make_image_file(), save=True)
    return item


@pytest.fixture
def review(db, media_item, user):
    return MediaItemReview.objects.create(
        media_item=media_item, user=user, content="Первый комментарий"
    )


@pytest.fixture
def about(db):
    return About.objects.create(body="О проекте", body_ru="О проекте")
