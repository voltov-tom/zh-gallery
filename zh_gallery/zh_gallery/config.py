import os

from dotenv import load_dotenv

load_dotenv()

DJANGO_ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS').split(',')
DEBUG = os.getenv('DEBUG')
SECRET_KEY = os.getenv('SECRET_KEY')
OAUTH2_GOOGLE = os.getenv('OAUTH2_GOOGLE')
OAUTH2_GOOGLE_SECRET = os.getenv('OAUTH2_GOOGLE_SECRET')
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS').split(',')

SQL_ENGINE = os.getenv('SQL_ENGINE')
SQL_DATABASE = os.getenv('SQL_DATABASE')
SQL_USER = os.getenv('SQL_USER')
SQL_PASSWORD = os.getenv('SQL_PASSWORD')
SQL_HOST = os.getenv('SQL_HOST')
SQL_PORT = os.getenv('SQL_PORT')
DATABASE = os.getenv('DATABASE')

EMAIL_USE_SSL = os.getenv('EMAIL_USE_SSL')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_CONFIRMATION_COOLDOWN = os.getenv('EMAIL_CONFIRMATION_COOLDOWN')
