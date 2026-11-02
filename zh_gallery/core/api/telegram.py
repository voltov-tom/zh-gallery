"""JSON API для Telegram-бота.

Раньше здесь был ``media_item.views += 1`` без сохранения (ответ обещал
просмотр, которого не было), пустая база роняла ``random.choice``, а ссылка
склеивалась из захардкоженного домена. Теперь всё через сервисы и
``request.build_absolute_uri``.
"""

from __future__ import annotations

from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET

from core import selectors, services
from core.models import MediaItem


def _bot_token_is_valid(request) -> bool:
    """Если TELEGRAM_BOT_TOKEN задан — требуем его в заголовке X-Bot-Token."""
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        return True
    return request.headers.get("X-Bot-Token") == token


def _media_item_payload(request, media_item: MediaItem) -> dict:
    return {
        "mediaItemUrl": request.build_absolute_uri(media_item.image.url),
        "title": media_item.title,
        "likes": media_item.likes.count(),
        "description": media_item.description,
        "views": media_item.views,
    }


@require_GET
def telegram_bot_get_media_item(request, slug):
    if not _bot_token_is_valid(request):
        return JsonResponse({"success": False, "error": "forbidden"}, status=403)

    media_item = get_object_or_404(MediaItem, slug=slug)
    services.register_view(media_item)
    return JsonResponse(_media_item_payload(request, media_item))


@require_GET
def telegram_bot_get_random_item(request):
    if not _bot_token_is_valid(request):
        return JsonResponse({"success": False, "error": "forbidden"}, status=403)

    media_item = selectors.get_random_media_item()
    if media_item is None:
        return JsonResponse({"success": False, "error": "gallery is empty"}, status=404)

    services.register_view(media_item)
    return JsonResponse(_media_item_payload(request, media_item))
