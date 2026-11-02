"""Корневая URL-конфигурация проекта."""

from __future__ import annotations

import re

from django.conf import settings
from django.contrib import admin
from django.urls import include, path, re_path

from core.views.media import media_file

urlpatterns = [
    path("admin/", admin.site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path("accounts/", include("allauth.urls")),
    path("", include("userprofile.urls")),
    path("", include("core.urls")),
]

# Медиа отдаёт Django: для Nextcloud иначе файлы недоступны (их нет на диске),
# а для локального хранилища этот маршрут перекрывает nginx. При DEBUG=True
# Django и сам раздаёт /media/, поэтому маршрут не нужен.
if not settings.DEBUG and settings.MEDIA_URL.startswith("/"):
    media_prefix = re.escape(settings.MEDIA_URL.strip("/"))
    urlpatterns.insert(0, re_path(rf"^{media_prefix}/(?P<path>.+)$", media_file, name="media_file"))

admin.site.site_header = "zh-gallery"
admin.site.site_title = "zh-gallery"
admin.site.index_title = "Управление галереей"
