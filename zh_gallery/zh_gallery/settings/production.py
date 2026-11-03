"""Настройки для docker/прода.

Безопасные значения включены по умолчанию, но всё, что ломает запуск без TLS
(редирект на https и secure-cookie), управляется переменными окружения —
иначе локальный docker-compose на http://localhost:8080 не открылся бы.
"""

import logging

from django.core.exceptions import ImproperlyConfigured

from .base import *  # noqa: F401,F403
from .base import INSECURE_SECRET_KEY, env

DEBUG = False

if SECRET_KEY == INSECURE_SECRET_KEY:
    raise ImproperlyConfigured(
        "SECRET_KEY не задан. Сгенерируйте его, например: "
        'python -c "from django.core.management.utils import get_random_secret_key '
        'as g; print(g())"'
    )

if not ALLOWED_HOSTS:
    raise ImproperlyConfigured("DJANGO_ALLOWED_HOSTS пуст — Django не примет ни один запрос.")

EMAIL_BACKEND = env.str("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")

# Хешированные имена статики: кэш на год и защита от stale-файлов
STORAGES["staticfiles"] = {
    "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage",
}

# Включать, когда сайт реально работает по https (за nginx/прокси)
SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT", default=False)
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE", default=False)
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE", default=False)
SECURE_HSTS_SECONDS = env.int("SECURE_HSTS_SECONDS", default=0)
SECURE_HSTS_INCLUDE_SUBDOMAINS = SECURE_HSTS_SECONDS > 0
SECURE_HSTS_PRELOAD = SECURE_HSTS_SECONDS > 0
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = "same-origin"
X_FRAME_OPTIONS = "DENY"

LOG_LEVEL = env.str("LOG_LEVEL", default="INFO")

if not SECURE_SSL_REDIRECT:
    logging.getLogger(__name__).warning(
        "SECURE_SSL_REDIRECT=False: сайт отдаётся по HTTP. После настройки TLS "
        "включите SECURE_SSL_REDIRECT, SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE "
        "и SECURE_HSTS_SECONDS (см. .env.example)."
    )
