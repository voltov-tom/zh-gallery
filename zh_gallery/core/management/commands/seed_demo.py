"""Наполнение БД демо-данными: удобно для локального запуска и проверки UI.

Пример::

    python manage.py seed_demo            # создаст категории и 12 картинок
    python manage.py seed_demo --reset    # предварительно удалит старые демо-данные

Картинки генерируются Pillow-ом, поэтому внешние файлы не нужны.
"""

from __future__ import annotations

import io
import random

from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.db import transaction
from PIL import Image, ImageDraw

from core.models import About, MainCategory, MediaItem, MediaItemReview, SubCategory

DEMO_DATA = {
    "Живопись": {
        "Портреты": ["Тихий взгляд", "Осенний свет", "Письмо"],
        "Пейзажи": ["Река утром", "Поле после дождя"],
    },
    "Фотография": {
        "Город": ["Ночной проспект", "Крыши"],
        "Природа": ["Туман", "Камни у воды"],
    },
}

PALETTE = [
    (174, 115, 148),
    (110, 140, 180),
    (150, 180, 140),
    (200, 160, 110),
    (120, 120, 140),
]


def make_image(title: str) -> ContentFile:
    """Генерирует простую картинку-заглушку с подписью."""
    width, height = 800, 600
    color = random.choice(PALETTE)
    image = Image.new("RGB", (width, height), color)
    draw = ImageDraw.Draw(image)
    draw.rectangle([40, 40, width - 40, height - 40], outline=(255, 255, 255), width=4)
    draw.text((60, 60), title, fill=(255, 255, 255))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=85)
    return ContentFile(buffer.getvalue(), name="demo.jpg")


class Command(BaseCommand):
    help = "Создаёт демонстрационные категории, картинки и комментарии"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Удалить созданные ранее демо-данные перед наполнением",
        )
        parser.add_argument("--username", default="demo", help="Имя пользователя для отзывов")

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        username = options["username"]

        if options["reset"]:
            MainCategory.objects.all().delete()
            About.objects.all().delete()
            self.stdout.write("Старые категории и страница «О проекте» удалены")

        user, created = User.objects.get_or_create(
            username=username, defaults={"email": f"{username}@example.com"}
        )
        if created:
            user.set_password("demo-password-12345")
            user.save(update_fields=["password"])
            self.stdout.write(f"Создан пользователь {username} / demo-password-12345")

        # ACCOUNT_EMAIL_VERIFICATION="mandatory": без подтверждённого адреса
        # allauth не пустит демо-пользователя на сайт.
        EmailAddress.objects.update_or_create(
            user=user,
            email=user.email,
            defaults={"verified": True, "primary": True},
        )

        about, _ = About.objects.get_or_create(pk=1)
        about.body_ru = (
            "zh-gallery — учебный проект: галерея работ творческого человека. "
            "Здесь можно смотреть работы, ставить лайки и оставлять комментарии."
        )
        about.body_en = (
            "zh-gallery is a study project: a gallery for a creative person's work. "
            "Browse, like and comment."
        )
        about.save()

        created_items = 0
        for category_title, subcategories in DEMO_DATA.items():
            category, _ = MainCategory.objects.get_or_create(title=category_title)
            for subcategory_title, item_titles in subcategories.items():
                subcategory, _ = SubCategory.objects.get_or_create(
                    category=category, title=subcategory_title
                )
                for title in item_titles:
                    if MediaItem.objects.filter(subcategory=subcategory, title=title).exists():
                        continue
                    item = MediaItem(
                        subcategory=subcategory,
                        title=title,
                        description=f"Демо-работа «{title}»",
                    )
                    item.image.save(f"{item.slug or title}.jpg", make_image(title))
                    item.save()
                    MediaItemReview.objects.create(
                        media_item=item,
                        user=user,
                        content=f"Демо-комментарий к работе «{title}»",
                    )
                    created_items += 1

        self.stdout.write(self.style.SUCCESS(f"Готово: добавлено {created_items} медиа-элементов"))
