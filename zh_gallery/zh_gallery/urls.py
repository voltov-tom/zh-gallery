from django.contrib import admin
from django.contrib.auth import views
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include

from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('logout/', views.LogoutView.as_view(next_page='/'), name='logout'),

    path('', frontpage_view, name='frontpage_view'),
    path('about/', about_view, name='about_view'),
    path('terms-and-conditions/', terms_and_conditions_view, name='terms_and_conditions_view'),
    path('privacy-policy/', privacy_policy_view, name='privacy_policy_view'),

    path('<slug:slug>/', category_view, name='category_view'),
    path('<slug:category_slug>/<slug:slug>/', subcategory_view, name='subcategory_view'),
    path('<slug:category_slug>/<slug:subcategory_slug>/<slug:slug>/', media_item_view, name='media_item_view'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
