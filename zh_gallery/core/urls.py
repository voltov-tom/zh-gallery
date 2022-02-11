from django.contrib.sitemaps.views import sitemap
from django.urls import path

from .sitemaps import StaticViewSitemap, SubCategorySitemap, MediaItemSitemap, MainCategorySitemap
from .views import frontpage_view, about_view, terms_and_conditions_view, privacy_policy_view, category_view, \
    subcategory_view, media_item_view
from .api import like_button, delete_review, edit_review

sitemaps = {
    'static': StaticViewSitemap,
    'category': MainCategorySitemap,
    'subcategory': SubCategorySitemap,
    'media_item': MediaItemSitemap,
}

urlpatterns = [
    path('', frontpage_view, name='frontpage_view'),
    path('about/', about_view, name='about_view'),
    path('terms-and-conditions/', terms_and_conditions_view, name='terms_and_conditions_view'),
    path('privacy-policy/', privacy_policy_view, name='privacy_policy_view'),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('api/like/', like_button, name='like_button'),
    path('api/delete-review/', delete_review, name='delete_review'),
    path('api/edit-review/', edit_review, name='edit_review'),

    path('<slug:slug>/', category_view, name='category_view'),
    path('<slug:category_slug>/<slug:slug>/', subcategory_view, name='subcategory_view'),
    path('<slug:category_slug>/<slug:subcategory_slug>/<slug:slug>/', media_item_view, name='media_item_view'),
]
