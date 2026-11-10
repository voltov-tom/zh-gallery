"""Базовые настройки, общие для всех окружений.

Все значения читаются из переменных окружения (или из файла ``.env`` в корне
репозитория). Конкретное окружение подключает этот модуль и переопределяет
только то, что от него зависит:

* ``zh_gallery.settings.local``      — разработка на машине;
* ``zh_gallery.settings.production`` — docker/прод;
* ``zh_gallery.settings.test``       — автотесты (pytest).

Такой подход убирает магию ``from .config import *`` и не позволяет забыть
обязательную переменную: django-environ сразу падает с понятной ошибкой.
"""

from __future__ import annotations

from pathlib import Path

import environ

# repo/zh_gallery/zh_gallery/settings/base.py -> repo/zh_gallery
BASE_DIR = Path(__file__).resolve().parents[2]
# корень репозитория: там лежат .env, docker-compose.yml, pyproject.toml
REPO_DIR = BASE_DIR.parent

env = environ.Env()
environ.Env.read_env(REPO_DIR / ".env")

# Заглушка, чтобы `manage.py check` и тесты работали без .env.
# production-настройки отказываются стартовать с этим значением.
INSECURE_SECRET_KEY = "django-insecure-dev-only-change-me"


def env_list(name: str, default: str = "") -> list[str]:
    """Прочитать список из строки через запятую, выбросив пустые элементы."""
    raw = env.str(name, default=default)
    return [item.strip() for item in raw.split(",") if item.strip()]


# ---------------------------------------------------------------------------
# Основное
# ---------------------------------------------------------------------------
SECRET_KEY = env.str("SECRET_KEY", default=INSECURE_SECRET_KEY)
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", default="localhost,127.0.0.1,[::1]")
CSRF_TRUSTED_ORIGINS = env_list("CSRF_TRUSTED_ORIGINS")

# nginx терминирует TLS и передаёт исходную схему в этом заголовке
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "django.contrib.sites",
    "django.forms",
    # modeltranslation должен идти раньше django.contrib.admin: его ready()
    # регистрирует переводы, а админка автодискаверит admin.py уже после.
    "modeltranslation",
    "django.contrib.admin",
    # сторонние
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.vk",
    "allauth.socialaccount.providers.mailru",
    # локальные
    "core",
    "userprofile",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "zh_gallery.urls"
WSGI_APPLICATION = "zh_gallery.wsgi.application"
ASGI_APPLICATION = "zh_gallery.asgi.application"

# Нужен, чтобы переопределять рендеринг ошибок форм шаблоном
# templates/django/forms/errors/list/ul.html
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.site_context",
            ],
        },
    },
]


# ---------------------------------------------------------------------------
# База данных
# ---------------------------------------------------------------------------
# Приоритет у DATABASE_URL (стандартный для деплоя формат), иначе собираем
# из привычных SQL_* переменных — так старый .env продолжает работать.
if env.str("DATABASE_URL", default=""):
    DATABASES = {"default": env.db_url("DATABASE_URL")}
else:
    DATABASES = {
        "default": {
            "ENGINE": env.str("SQL_ENGINE", default="django.db.backends.postgresql"),
            "NAME": env.str("SQL_DATABASE", default="zh_gallery"),
            "USER": env.str("SQL_USER", default="zh_gallery"),
            "PASSWORD": env.str("SQL_PASSWORD", default=""),
            "HOST": env.str("SQL_HOST", default="localhost"),
            "PORT": env.str("SQL_PORT", default="5432"),
            "CONN_MAX_AGE": env.int("SQL_CONN_MAX_AGE", default=60),
            "CONN_HEALTH_CHECKS": True,
        }
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ---------------------------------------------------------------------------
# Аутентификация
# ---------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LOGIN_URL = "account_login"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

SITE_ID = 1
# Домен и имя сайта: используются django.contrib.sites и allauth для абсолютных
# ссылок в письмах. После migrate объект Site приводится к этим значениям.
SITE_DOMAIN = env.str("SITE_DOMAIN", default="zh-gallery.ru")
# Версия политики обработки ПДн: попадает в запись согласия.
# При изменении текста политики поднимите и это значение.
PRIVACY_POLICY_VERSION = env.str("PRIVACY_POLICY_VERSION", default="2026-11-02")
SITE_NAME = env.str("SITE_NAME", default="zh-gallery")

# django-allauth 65.x
ACCOUNT_LOGIN_METHODS = {"username", "email"}
# Регистрация открывается/закрывается одной переменной окружения.
# Пока продумываем антиспам — на проде выключена.
SIGNUP_ENABLED = env.bool("SIGNUP_ENABLED", default=True)
ACCOUNT_SIGNUP_FIELDS = ["email*", "username*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = "/"
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = "/"
ACCOUNT_USERNAME_MIN_LENGTH = 3
# Кастомный адаптер: в проекте только HTML-шаблоны писем (*.html, без *.txt)
ACCOUNT_ADAPTER = "core.adapters.AccountAdapter"
ACCOUNT_FORMS = {
    "signup": "userprofile.forms.SignupFormAllAuth",
    "login": "userprofile.forms.LoginFormAllAuth",
    "add_email": "userprofile.forms.AddEmailFormAllAuth",
    "change_password": "userprofile.forms.ChangePasswordFormAllAuth",
    "set_password": "userprofile.forms.SetPasswordFormAllAuth",
    "reset_password": "userprofile.forms.ResetPasswordFormAllAuth",
    "reset_password_from_key": "userprofile.forms.ResetPasswordKeyFormAllAuth",
}

# Вход через российские сервисы. Учётные данные можно задать в .env
# (APP-блок ниже) или создать SocialApp в админке — allauth поймёт оба варианта.
SOCIALACCOUNT_PROVIDERS = {
    "vk": {
        "SCOPE": ["email"],
        "AUTH_PARAMS": {"response_type": "code"},
    },
    "mailru": {
        "SCOPE": ["email"],
    },
}

if env.str("VK_CLIENT_ID", default=""):
    SOCIALACCOUNT_PROVIDERS["vk"]["APP"] = {
        "client_id": env.str("VK_CLIENT_ID"),
        "secret": env.str("VK_SECRET", default=""),
    }
if env.str("MAILRU_CLIENT_ID", default=""):
    SOCIALACCOUNT_PROVIDERS["mailru"]["APP"] = {
        "client_id": env.str("MAILRU_CLIENT_ID"),
        "secret": env.str("MAILRU_SECRET", default=""),
    }


# ---------------------------------------------------------------------------
# Почта
# ---------------------------------------------------------------------------
EMAIL_BACKEND = env.str("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = env.str("EMAIL_HOST", default="localhost")
EMAIL_PORT = env.int("EMAIL_PORT", default=25)
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="")
# Яндекс требует пароль приложения; допускаем и алиас YANDEX_MAIL_TOKEN
EMAIL_HOST_PASSWORD = env.str(
    "EMAIL_HOST_PASSWORD", default=env.str("YANDEX_MAIL_TOKEN", default="")
)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", default="zh-gallery@localhost")
# Куда пересылаются сообщения, отправленные через Telegram-бота
CONTACT_EMAIL = env.str("CONTACT_EMAIL", default="zhenya@zh-gallery.ru")

# --- генерация описаний работ через vision-модель -------------------------
# Ключ не коммитим: он живёт только в .env на сервере/машине разработчика
AI_API_KEY = env.str("AI_API_KEY", default="")
AI_BASE_URL = env.str("AI_BASE_URL", default="https://api.deepseek.com")
AI_MODEL = env.str("AI_MODEL", default="deepseek-flash")
AI_TIMEOUT = env.int("AI_TIMEOUT", default=120)
AI_MAX_TOKENS = env.int("AI_MAX_TOKENS", default=2500)
SERVER_EMAIL = DEFAULT_FROM_EMAIL
# сколько секунд ждать между повторными письмами подтверждения
EMAIL_CONFIRMATION_COOLDOWN = env.int("EMAIL_CONFIRMATION_COOLDOWN", default=60)


# ---------------------------------------------------------------------------
# Кэш и сессии
# ---------------------------------------------------------------------------
REDIS_URL = env.str("REDIS_URL", default="")
if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "SOCKET_CONNECT_TIMEOUT": 5,
                "SOCKET_TIMEOUT": 5,
                "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",
                "IGNORE_EXCEPTIONS": True,
            },
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
else:
    CACHES = {
        "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.db"

SESSION_COOKIE_AGE = 60 * 60 * 24 * 14
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True  # JS берёт токен из <meta name="csrf-token">


# ---------------------------------------------------------------------------
# Локализация
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "ru"
LANGUAGES = (("ru", "Russian"), ("en", "English"))
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = "Europe/Samara"
USE_I18N = True
USE_TZ = True


# ---------------------------------------------------------------------------
# Статика и медиа
# ---------------------------------------------------------------------------
STATIC_URL = env.str("STATIC_URL", default="/static/")
STATIC_ROOT = Path(env.str("STATIC_ROOT", default=str(BASE_DIR / "static")))

MEDIA_URL = env.str("MEDIA_URL", default="/media/")
MEDIA_ROOT = Path(env.str("MEDIA_ROOT", default=str(BASE_DIR / "media")))

# local | nextcloud. Для nextcloud файлы хранятся в WebDAV, а не на диске.
MEDIA_STORAGE = env.str("MEDIA_STORAGE", default="local").lower()

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
        "OPTIONS": {"location": MEDIA_ROOT, "base_url": MEDIA_URL},
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

if MEDIA_STORAGE == "nextcloud":
    STORAGES["default"] = {"BACKEND": "core.storage.NextcloudStorage", "OPTIONS": {}}

# Локальный кэш картинок: нужен, чтобы сайт продолжал показывать работы
# при недоступном Nextcloud. Для локального диска выключен — файлы и так рядом.
MEDIA_CACHE_ENABLED = env.bool("MEDIA_CACHE_ENABLED", default=(MEDIA_STORAGE != "local"))
MEDIA_CACHE_ROOT = Path(env.str("MEDIA_CACHE_ROOT", default=str(BASE_DIR / "media-cache")))
# Длинная сторона отдаваемой картинки: оригиналы с камеры весят 3–7 МБ
MEDIA_SERVE_MAX_SIDE = env.int("MEDIA_SERVE_MAX_SIDE", default=1600)
MEDIA_SERVE_QUALITY = env.int("MEDIA_SERVE_QUALITY", default=82)

# Nextcloud / WebDAV. Старые имена WEBDAV_* оставлены для совместимости.
# HOSTNAME может быть как доменом, так и полным адресом WebDAV-корня
# (https://host/remote.php/dav/files/user/) — второй вариант поддерживается.
NEXTCLOUD_HOSTNAME = env.str("NEXTCLOUD_HOSTNAME", default=env.str("WEBDAV_HOSTNAME", default=""))
NEXTCLOUD_BASE_URL = env.str("NEXTCLOUD_BASE_URL", default="")
NEXTCLOUD_LOGIN = env.str("NEXTCLOUD_LOGIN", default=env.str("WEBDAV_LOGIN", default=""))
NEXTCLOUD_PASSWORD = env.str("NEXTCLOUD_PASSWORD", default=env.str("WEBDAV_PASSWORD", default=""))
NEXTCLOUD_ROOT = env.str("NEXTCLOUD_ROOT", default=env.str("WEBDAV_ROOT", default="zh-gallery"))
# Публичный префикс, по которому браузер получает файлы (публичная ссылка/nginx).
# Если не задан — используется MEDIA_URL.
NEXTCLOUD_PUBLIC_URL = env.str("NEXTCLOUD_PUBLIC_URL", default="")
NEXTCLOUD_TIMEOUT = env.int("NEXTCLOUD_TIMEOUT", default=30)

# ---------------------------------------------------------------------------
# Telegram-бот (JSON API /api/telegram_bot/...)
# ---------------------------------------------------------------------------
# Если токен задан, эндпоинты требуют заголовок X-Bot-Token. Пустое значение
# оставляет API открытым — так работают уже установленные клиенты.
TELEGRAM_BOT_TOKEN = env.str("TELEGRAM_BOT_TOKEN", default="")


# ---------------------------------------------------------------------------
# Логирование
# ---------------------------------------------------------------------------
LOG_LEVEL = env.str("LOG_LEVEL", default="INFO")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {"handlers": ["console"], "level": LOG_LEVEL},
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "core.integrations.nextcloud": {
            "handlers": ["console"],
            "level": env.str("NEXTCLOUD_LOG_LEVEL", default="INFO"),
            "propagate": False,
        },
    },
}
