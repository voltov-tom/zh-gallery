"""ASGI-точка входа."""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "zh_gallery.settings.production")

application = get_asgi_application()
