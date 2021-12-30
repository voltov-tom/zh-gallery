from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path
from django.conf import settings

from core.views import frontpage_view, subcategory_view, about_view, category_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', frontpage_view, name='frontpage_view'),
    path('about', about_view, name='about_view'),
    path('<slug:slug>/', category_view, name='category_view'),
    path('<slug:category_slug>/<slug:slug>/', subcategory_view, name='subcategory_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
