"""JSON API галереи: лайки и комментарии.

Контракт ответов сохранён совместимым с мобильным клиентом и старой версией
фронтенда (ключи ``success``, ``liked``, ``likes_count``, ``media_id``), но
поверх него добавлены:

* корректные HTTP-статусы (400/403/404 вместо «200 и success:false»);
* устойчивый разбор JSON (раньше битый body или отсутствующий ключ давали 500);
* проверка владельца комментария (как и раньше) и ``select_for_update`` в лайках.
"""

from __future__ import annotations

import json
from functools import wraps

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from core import services
from core.models import MediaItem, MediaItemReview


class BadPayload(ValueError):
    """Тело запроса не соответствует ожидаемому формату."""


def _error(message: str, status: int = 400) -> JsonResponse:
    return JsonResponse({"success": False, "error": message}, status=status)


def parse_json(request) -> dict:
    """Разбирает JSON-тело запроса и требует, чтобы это был объект."""
    try:
        payload = json.loads(request.body or b"{}")
    except (json.JSONDecodeError, UnicodeDecodeError) as exc:
        raise BadPayload("invalid JSON body") from exc
    if not isinstance(payload, dict):
        raise BadPayload("JSON object expected")
    return payload


def json_login_required(view):
    """Как @login_required, но отвечает 403 JSON вместо редиректа на логин."""

    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return _error("authentication required", status=403)
        return view(request, *args, **kwargs)

    return wrapper


def _payload_or_error(request):
    """Возвращает (payload, None) либо (None, JsonResponse)."""
    try:
        return parse_json(request), None
    except BadPayload as exc:
        return None, _error(str(exc))


def _int_field(payload: dict, name: str) -> int:
    value = payload.get(name)
    try:
        return int(value)
    except (TypeError, ValueError) as exc:
        raise BadPayload(f"'{name}' must be an integer") from exc


@require_POST
@json_login_required
def like_button(request):
    """POST /api/like/ — поставить или снять лайк.

    Тело: ``{"media_id": 1}``. Поле ``operation`` из старого API игнорируется.
    """
    payload, error = _payload_or_error(request)
    if error:
        return error

    try:
        media_id = _int_field(payload, "media_id")
    except BadPayload as exc:
        return _error(str(exc))

    media_item = MediaItem.objects.filter(pk=media_id).first()
    if media_item is None:
        return _error("media item not found", status=404)

    liked = services.toggle_like(media_item, request.user)
    return JsonResponse(
        {
            "success": True,
            "liked": liked,
            "likes_count": media_item.likes.count(),
            "media_id": media_item.pk,
        }
    )


@require_POST
@json_login_required
def edit_review(request):
    """POST /api/edit-review/ — изменить свой комментарий.

    Тело: ``{"review_id": 1, "content": "..."}``.
    """
    payload, error = _payload_or_error(request)
    if error:
        return error

    try:
        review_id = _int_field(payload, "review_id")
        content = str(payload.get("content", "")).strip()
    except BadPayload as exc:
        return _error(str(exc))

    if not content:
        return _error("content cannot be empty")

    review = MediaItemReview.objects.filter(pk=review_id, user=request.user).first()
    if review is None:
        return _error("review not found", status=404)

    services.update_review(review, content)
    return JsonResponse({"success": True, "edited": review.edited, "content": review.content})


@require_POST
@json_login_required
def delete_review(request):
    """POST /api/delete-review/ — удалить свой комментарий."""
    payload, error = _payload_or_error(request)
    if error:
        return error

    try:
        review_id = _int_field(payload, "review_id")
    except BadPayload as exc:
        return _error(str(exc))

    review = MediaItemReview.objects.filter(pk=review_id, user=request.user).first()
    if review is None:
        return _error("review not found", status=404)

    services.delete_review(review)
    return JsonResponse({"success": True})
