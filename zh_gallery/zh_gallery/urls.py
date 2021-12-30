from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

from core.views import base_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', base_view, name='base_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
