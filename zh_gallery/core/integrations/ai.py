"""Описания работ через vision-модель (DeepSeek, OpenAI-совместимый API).

Модель принимает изображение как data-URI и возвращает JSON с описанием на
русском и английском. Ключ задаётся в ``AI_API_KEY`` и в репозиторий не попадает.
"""

from __future__ import annotations

import base64
import io
import json
import logging
import re

import requests
from django.conf import settings
from PIL import Image, UnidentifiedImageError

logger = logging.getLogger(__name__)

# Картинку перед отправкой уменьшаем: меньше токенов и стабильнее ответ
MAX_IMAGE_SIDE = 768
JPEG_QUALITY = 80

# Тело поля description — 255 символов, оставляем запас на «ёлочки» и тире
MAX_DESCRIPTION_LENGTH = 255

PROMPT = (
    "Ты — редактор художественной галереи. Посмотри на изображение и напиши описание "
    "на русском: 2–3 предложения о свете, цвете, композиции и настроении, в конце — "
    "один короткий вопрос к зрителю. Не выдумывай имён, мест и событий. До 200 символов. "
    "Затем переведи на английский в том же тоне, до 220 символов. "
    'Верни строго JSON: {"ru": "...", "en": "..."}'
)


class AIDescriptionError(Exception):
    """Не удалось получить описание — старые значения остаются как были."""


def _image_data_uri(media_item) -> str:
    """Читает файл работы, уменьшает и превращает в data-URI для API."""
    try:
        with media_item.image.open("rb") as source:
            raw = source.read()
        image = Image.open(io.BytesIO(raw)).convert("RGB")
    except (UnidentifiedImageError, OSError) as error:
        raise AIDescriptionError(f"не удалось прочитать изображение: {error}") from error

    image.thumbnail((MAX_IMAGE_SIDE, MAX_IMAGE_SIDE))
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=JPEG_QUALITY)
    encoded = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/jpeg;base64,{encoded}"


def _strip_code_fences(text: str) -> str:
    """Модель иногда оборачивает JSON в ```json ... ``` — срезаем обёртку."""
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    return re.sub(r"\s*```$", "", text).strip()


def _parse_response(content: str) -> dict[str, str]:
    raw = _strip_code_fences(content)
    try:
        payload = json.loads(raw)
    except ValueError as error:
        match = re.search(r"\{.*\}", raw, re.S)
        if not match:
            raise AIDescriptionError("модель вернула не JSON") from error
        try:
            payload = json.loads(match.group(0))
        except ValueError as nested:
            raise AIDescriptionError("модель вернула битый JSON") from nested

    if not isinstance(payload, dict):
        raise AIDescriptionError("модель вернула не объект")

    texts = {}
    for language in ("ru", "en"):
        value = str(payload.get(language) or "").strip()
        if not value:
            raise AIDescriptionError(f"в ответе нет поля {language}")
        texts[language] = value[:MAX_DESCRIPTION_LENGTH]
    return texts


def _call_api(payload: dict) -> str:
    """Один запрос к API. Возвращает content ответа модели."""
    url = f"{settings.AI_BASE_URL.rstrip('/')}/chat/completions"
    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Authorization": f"Bearer {settings.AI_API_KEY}"},
            timeout=settings.AI_TIMEOUT,
        )
    except requests.RequestException as error:
        logger.warning("ИИ недоступно (%s): %s", url, error)
        raise AIDescriptionError("сервис ИИ недоступен, попробуйте позже") from error

    if response.status_code != 200:
        logger.warning("ИИ вернуло %s: %s", response.status_code, response.text[:200])
        raise AIDescriptionError(f"сервис ИИ ответил {response.status_code}")

    try:
        body = response.json()
    except ValueError as error:
        raise AIDescriptionError("сервис ИИ вернул не JSON") from error

    choices = body.get("choices") or []
    return ((choices[0].get("message") or {}).get("content") or "") if choices else ""


def request_description(media_item) -> dict[str, str]:
    """Запрос к модели. Ничего не сохраняет — только возвращает тексты."""
    if not settings.AI_API_KEY:
        raise AIDescriptionError("не задан AI_API_KEY — генерация отключена")

    payload = {
        "model": settings.AI_MODEL,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {"type": "image_url", "image_url": {"url": _image_data_uri(media_item)}},
                ],
            }
        ],
        "max_tokens": settings.AI_MAX_TOKENS,
        "effort": "low",
    }

    content = _call_api(payload)
    if not content:
        # модель иногда тратит весь лимит на «рассуждение» — пробуем ещё раз
        # с удвоенным лимитом, прежде чем сдаться
        logger.info("пустой ответ ИИ, повтор с увеличенным лимитом")
        payload["max_tokens"] = settings.AI_MAX_TOKENS * 2
        content = _call_api(payload)

    if not content:
        raise AIDescriptionError("модель вернула пустой ответ")

    return _parse_response(content)
