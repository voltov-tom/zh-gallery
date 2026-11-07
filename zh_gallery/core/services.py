"""Сервисы — операции, которые меняют состояние.

Вьюхи и API вызывают только их: так логика лайков/отзывов не дублируется
между HTML-страницами, JSON API и Telegram-ботом.
"""

from __future__ import annotations

from django.db import transaction
from django.db.models import F
from django.utils import timezone

from .integrations.ai import request_description
from .models import MediaItem, MediaItemReview


def register_view(media_item: MediaItem) -> int:
    """Атомарно увеличивает счётчик просмотров и возвращает новое значение."""
    MediaItem.objects.filter(pk=media_item.pk).update(views=F("views") + 1)
    media_item.refresh_from_db(fields=["views"])
    return media_item.views


@transaction.atomic
def toggle_like(media_item: MediaItem, user) -> bool:
    """Ставит или снимает лайк. Возвращает True, если лайк поставлен.

    ``select_for_update`` защищает от гонки при двойном клике: два параллельных
    запроса не создадут «двойной» лайк и не разойдутся по счётчику.
    """
    locked = MediaItem.objects.select_for_update().get(pk=media_item.pk)

    if locked.likes.filter(pk=user.pk).exists():
        locked.likes.remove(user)
        liked = False
    else:
        locked.likes.add(user)
        locked.like_time = timezone.now()
        locked.save(update_fields=["like_time"])
        liked = True

    media_item.refresh_from_db(fields=["like_time"])
    return liked


def create_review(media_item: MediaItem, user, content: str) -> MediaItemReview:
    return MediaItemReview.objects.create(media_item=media_item, user=user, content=content.strip())


def update_review(review: MediaItemReview, content: str) -> MediaItemReview:
    """Обновляет текст отзыва и помечает его как отредактированный."""
    content = content.strip()
    if review.content != content:
        review.content = content
        review.edited = True
        review.save(update_fields=["content", "edited"])
    return review


def delete_review(review: MediaItemReview) -> None:
    review.delete()


def generate_media_description(media_item: MediaItem) -> dict[str, str]:
    """Просит ИИ описание работы и сохраняет его в оба языка.

    Старые значения не трогаем, пока модель не вернула оба текста: если сервис
    недоступен, в базе остаётся то, что было.
    """
    texts = request_description(media_item)
    MediaItem.objects.filter(pk=media_item.pk).update(
        description_ru=texts["ru"],
        description_en=texts["en"],
        description_generated_by_ai=True,
    )
    media_item.description_ru = texts["ru"]
    media_item.description_en = texts["en"]
    media_item.description_generated_by_ai = True
    return texts
