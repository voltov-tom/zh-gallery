"""Настройки для автотестов: максимально быстро и без внешних сервисов."""

import atexit
import shutil
import tempfile

from .base import *  # noqa: F401,F403
from .base import BASE_DIR

DEBUG = False

SECRET_KEY = "test-secret-key-not-for-production"
ALLOWED_HOSTS = ["*"]

# SQLite в памяти + быстрый хешер паролей
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
EMAIL_HOST = "localhost"

CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"

# Файлы пишем во временную папку, а не в репозиторий
_TEST_MEDIA_ROOT = tempfile.mkdtemp(prefix="zh-gallery-tests-")
atexit.register(shutil.rmtree, _TEST_MEDIA_ROOT, ignore_errors=True)

MEDIA_ROOT = _TEST_MEDIA_ROOT
MEDIA_STORAGE = "local"
# Кэш медиа в тестах выключен; включаем точечно через override_settings
MEDIA_CACHE_ENABLED = False
MEDIA_CACHE_ROOT = _TEST_MEDIA_ROOT + "-cache"
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {"location": MEDIA_ROOT, "base_url": MEDIA_URL},
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# Тесты не должны ходить в Nextcloud и слать реальные письма
NEXTCLOUD_HOSTNAME = ""
TELEGRAM_BOT_TOKEN = ""

LOCALE_PATHS = [BASE_DIR / "locale"]

LOGGING["root"]["level"] = "WARNING"  # noqa: F405
