"""Приведение картинок к «веб-размеру» перед отдачей.

Фотографии с камеры весят 3–7 МБ. Раскладка «как есть» даёт страницу на
десятки мегабайт и медленную первую отрисовку, поэтому в кэш (и в ответ)
кладётся уменьшенная копия: длинная сторона не больше ``MEDIA_SERVE_MAX_SIDE``,
JPEG с качеством ``MEDIA_SERVE_QUALITY``. Оригиналы в Nextcloud не трогаем.
"""

from __future__ import annotations

import io
import logging

from django.conf import settings
from PIL import Image, UnidentifiedImageError

logger = logging.getLogger(__name__)

JPEG_QUALITY = 82
MAX_SIDE = 1600


def _max_side() -> int:
    return int(getattr(settings, "MEDIA_SERVE_MAX_SIDE", MAX_SIDE))


def _quality() -> int:
    return int(getattr(settings, "MEDIA_SERVE_QUALITY", JPEG_QUALITY))


def is_shrinkable(name: str) -> bool:
    """Сжимаем только растровые форматы, которые умеет Pillow."""
    return name.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))


def shrink(payload: bytes, name: str = "") -> bytes:
    """Уменьшает картинку до веб-размера.

    Возвращает исходные байты, если файл уже маленький, формат не растровый,
    Pillow не смог его прочитать или что-то пошло не так — отдача картинки
    важнее экономии трафика.
    """
    if not payload or (name and not is_shrinkable(name)):
        return payload

    try:
        with Image.open(io.BytesIO(payload)) as image:
            image.load()
            width, height = image.size
            limit = _max_side()
            if max(width, height) <= limit:
                return payload

            image.thumbnail((limit, limit), Image.LANCZOS)

            if image.mode in ("RGBA", "LA", "P"):
                # прозрачность на JPEG не переносится — кладём на белый фон
                rgba = image.convert("RGBA")
                background = Image.new("RGB", rgba.size, (255, 255, 255))
                background.paste(rgba, mask=rgba.split()[-1])
                image = background
            else:
                image = image.convert("RGB")

            buffer = io.BytesIO()
            image.save(buffer, format="JPEG", quality=_quality(), optimize=True)
            result = buffer.getvalue()
            return result if len(result) < len(payload) else payload
    except (UnidentifiedImageError, OSError, ValueError) as error:
        logger.warning("Не удалось уменьшить %s: %s", name or "картинку", error)
        return payload
