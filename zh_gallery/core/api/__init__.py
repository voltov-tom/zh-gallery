"""Публичный интерфейс JSON API (для core/urls.py)."""

from .gallery import delete_review, edit_review, like_button
from .telegram import telegram_bot_get_media_item, telegram_bot_get_random_item

__all__ = [
    "delete_review",
    "edit_review",
    "like_button",
    "telegram_bot_get_media_item",
    "telegram_bot_get_random_item",
]
