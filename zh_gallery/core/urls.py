from django.urls import path

from .api import like
from .views import frontpage_view, about_view, terms_and_conditions_view, privacy_policy_view, category_view, \
    subcategory_view, media_item_view

urlpatterns = [
    path('', frontpage_view, name='frontpage_view'),
    path('about/', about_view, name='about_view'),
    path('terms-and-conditions/', terms_and_conditions_view, name='terms_and_conditions_view'),
    path('privacy-policy/', privacy_policy_view, name='privacy_policy_view'),

    path('<slug:slug>/', category_view, name='category_view'),
    path('<slug:category_slug>/<slug:slug>/', subcategory_view, name='subcategory_view'),
    path('<slug:category_slug>/<slug:subcategory_slug>/<slug:slug>/', media_item_view, name='media_item_view'),

    path('api/like/', like, name='media_like'),
]
