"""URL-конфигурация приложения core.

Порядок важен: служебные и API-пути объявлены раньше «жадных» slug-маршрутов.
Имена маршрутов сохранены прежними — на них ссылаются шаблоны, sitemap и
внешние клиенты.
"""

from __future__ import annotations

from django.contrib.sitemaps.views import sitemap
from django.urls import path
from django.views.generic import TemplateView

from .api import (
    delete_review,
    edit_review,
    like_button,
    telegram_bot_get_media_item,
    telegram_bot_get_random_item,
    telegram_bot_send_contact,
)
from .sitemaps import (
    MainCategorySitemap,
    MediaItemSitemap,
    StaticViewSitemap,
    SubCategorySitemap,
)
from .views import (
    AboutView,
    FrontPageView,
    MainCategoryDetailView,
    MediaItemDetailView,
    PrivacyPolicyView,
    SubCategoryDetailView,
    TermsAndConditionsView,
    healthcheck,
)

sitemaps = {
    "static": StaticViewSitemap,
    "category": MainCategorySitemap,
    "subcategory": SubCategorySitemap,
    "media_item": MediaItemSitemap,
}

urlpatterns = [
    path("", FrontPageView.as_view(), name="frontpage_view"),
    path("about/", AboutView.as_view(), name="about_view"),
    path(
        "terms-and-conditions/",
        TermsAndConditionsView.as_view(),
        name="terms_and_conditions_view",
    ),
    path("privacy-policy/", PrivacyPolicyView.as_view(), name="privacy_policy_view"),
    path("healthz/", healthcheck, name="healthcheck"),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots_txt",
    ),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
    # JSON API
    path("api/like/", like_button, name="like_button"),
    path("api/delete-review/", delete_review, name="delete_review"),
    path("api/edit-review/", edit_review, name="edit_review"),
    path(
        "api/telegram_bot/get_random_item/",
        telegram_bot_get_random_item,
        name="get_random_item",
    ),
    path(
        "api/telegram_bot/send_message/",
        telegram_bot_send_contact,
        name="telegram_bot_send_message",
    ),
    path(
        "api/telegram_bot/get_media_item/<slug:slug>/",
        telegram_bot_get_media_item,
        name="get_media_item",
    ),
    # Каталог: /категория/, /категория/подкатегория/, /категория/подкатегория/элемент/
    path("<slug:slug>/", MainCategoryDetailView.as_view(), name="category_view"),
    path(
        "<slug:category_slug>/<slug:slug>/",
        SubCategoryDetailView.as_view(),
        name="subcategory_view",
    ),
    path(
        "<slug:category_slug>/<slug:subcategory_slug>/<slug:slug>/",
        MediaItemDetailView.as_view(),
        name="media_item_view",
    ),
]
