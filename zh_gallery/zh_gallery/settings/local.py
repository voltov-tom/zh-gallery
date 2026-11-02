"""Настройки для разработки на локальной машине.

Запуск: ``DJANGO_SETTINGS_MODULE=zh_gallery.settings.local manage.py runserver``
(это значение по умолчанию в manage.py).
"""

from .base import *  # noqa: F401,F403
from .base import env

DEBUG = True

# В разработке удобно открывать проект с телефона в локальной сети
ALLOWED_HOSTS = ["*"]

EMAIL_BACKEND = env.str("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")

# Без Redis сессии хранятся в БД — профиль «всё локально одной командой»
if not REDIS_URL:
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}

INTERNAL_IPS = ["127.0.0.1", "localhost"]

# В dev не нужен манифест статики
STORAGES["staticfiles"] = {
    "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
}
