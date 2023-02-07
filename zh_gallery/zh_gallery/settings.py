from .hidden_settings import *
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

OAuth2_google = OAUTH2_GOOGLE
OAuth2_google_secret = OAUTH2_GOOGLE_SECRET

SECRET_KEY = SECRET_KEY

DEBUG = DEBUG

ALLOWED_HOSTS = DJANGO_ALLOWED_HOSTS

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    'django.contrib.sites',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',

    'modeltranslation',
    'django.contrib.admin',

    'core',
    'userprofile',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    'django.middleware.locale.LocaleMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'zh_gallery.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR / "templates", ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',

                'core.context_processors.context',
            ],
        },
    },
]

WSGI_APPLICATION = 'zh_gallery.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': SQL_ENGINE,
        'NAME': SQL_DATABASE,
        'USER': SQL_USER,
        'PASSWORD': SQL_PASSWORD,
        'HOST': SQL_HOST,
        'PORT': SQL_PORT
    }
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_REQUIRED = True

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru'

LOCALE_PATHS = [
    BASE_DIR / 'allauth/locale',
    BASE_DIR / 'userprofile/locale',
    BASE_DIR / 'core/locale'
]

LANGUAGES = (
    ('ru', 'Russian'),
    ('en', 'English'),
)

TIME_ZONE = 'Europe/Samara'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static/'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# all_auth
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 3
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/'
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# EMAIL_USE_TLS = True
EMAIL_USE_SSL = EMAIL_USE_SSL,
EMAIL_HOST = EMAIL_HOST,
EMAIL_PORT = EMAIL_PORT,
EMAIL_HOST_USER = DEFAULT_FROM_EMAIL = EMAIL_HOST_USER,
EMAIL_HOST_PASSWORD = EMAIL_HOST_PASSWORD,
EMAIL_CONFIRMATION_COOLDOWN = EMAIL_CONFIRMATION_COOLDOWN,

ACCOUNT_FORMS = {
    'signup': 'userprofile.forms.SignupFormAllAuth',
    'login': 'userprofile.forms.LoginFormAllAuth',
    'add_email': 'userprofile.forms.AddEmailFormAllAuth',
    'change_password': 'userprofile.forms.ChangePasswordFormAllAuth',
    'set_password': 'userprofile.forms.SetPasswordFormAllAuth',
    'reset_password': 'userprofile.forms.ResetPasswordFormAllAuth',
    'reset_password_from_key': 'userprofile.forms.ResetPasswordKeyFormAllAuth',
}
