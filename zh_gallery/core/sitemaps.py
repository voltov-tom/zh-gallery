"""Карта сайта. Добавлены страницы медиа-элементов (их раньше не было)."""

from __future__ import annotations

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import MainCategory, MediaItem, SubCategory


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self) -> list[str]:
        return [
            "frontpage_view",
            "about_view",
            "terms_and_conditions_view",
            "privacy_policy_view",
        ]

    def location(self, item: str) -> str:
        return reverse(item)


class MainCategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return MainCategory.objects.all()


class SubCategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return SubCategory.objects.select_related("category")


class MediaItemSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return MediaItem.objects.select_related("subcategory", "subcategory__category")
