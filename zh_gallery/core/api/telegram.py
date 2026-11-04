"""JSON API для Telegram-бота.

Раньше здесь был ``media_item.views += 1`` без сохранения (ответ обещал
просмотр, которого не было), пустая база роняла ``random.choice``, а ссылка
склеивалась из захардкоженного домена. Теперь всё через сервисы и
``request.build_absolute_uri``.
"""

from __future__ import annotations

import json
import logging

from django.conf import settings
from django.core.cache import cache
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from core import selectors, services
from core.models import MediaItem

logger = logging.getLogger(__name__)

# Сообщение из бота: длина и лимит, чтобы не превращали бота в спам-канал
CONTACT_MESSAGE_MAX_LENGTH = 2000
CONTACT_RATE_LIMIT = 3
CONTACT_RATE_WINDOW = 600  # секунд


def _bot_token_is_valid(request) -> bool:
    """Эндпоинт работает только с настроенным токеном.

    Раньше при пустом TELEGRAM_BOT_TOKEN проверка пропускала всех: любой GET
    накручивал просмотры. Теперь без токена API выключено (fail closed).
    """
    token = settings.TELEGRAM_BOT_TOKEN
    if not token:
        return False
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


@csrf_exempt
@require_POST
def telegram_bot_send_contact(request):
    """Сообщение «Напишите мне» из бота — пересылаем на почту оператора.

    Аутентификация та же, что у остальных эндпоинтов бота: заголовок
    X-Bot-Token. CSRF отключён осознанно — бот не браузер, а токен проверяем.
    """
    if not _bot_token_is_valid(request):
        return JsonResponse({"success": False, "error": "forbidden"}, status=403)

    try:
        payload = json.loads(request.body or b"{}")
    except ValueError:
        return JsonResponse({"success": False, "error": "invalid json"}, status=400)
    if not isinstance(payload, dict):
        return JsonResponse({"success": False, "error": "invalid payload"}, status=400)

    text = str(payload.get("text") or "").strip()
    telegram_id = payload.get("telegram_id")
    # в теме письма не должно быть переносов строк — иначе заголовки подделываются
    username = str(payload.get("username") or "").replace("\r", " ").replace("\n", " ").strip()[:64]

    if not text or len(text) > CONTACT_MESSAGE_MAX_LENGTH:
        return JsonResponse({"success": False, "error": "invalid text"}, status=400)
    if not isinstance(telegram_id, int) or telegram_id <= 0:
        return JsonResponse({"success": False, "error": "invalid telegram id"}, status=400)

    rate_key = f"telegram-contact:{telegram_id}"
    sent_count = cache.get(rate_key, 0)
    if sent_count >= CONTACT_RATE_LIMIT:
        return JsonResponse({"success": False, "error": "too many messages"}, status=429)
    cache.set(rate_key, sent_count + 1, CONTACT_RATE_WINDOW)

    author = f"@{username}" if username else f"id {telegram_id}"
    subject = f"Сообщение из Telegram-бота: {author}"
    body = (
        f"От: {author} (telegram id {telegram_id})\n"
        f"Время: {timezone.localtime():%d.%m.%Y %H:%M}\n\n"
        f"{text}\n"
    )
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [settings.CONTACT_EMAIL])
    except Exception:
        logger.exception("не удалось отправить письмо из бота")
        return JsonResponse({"success": False, "error": "mail failed"}, status=500)

    return JsonResponse({"success": True})
