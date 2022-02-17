from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import MainCategory, SubCategory


def lastmod(obj):
    return obj.date_added


class StaticViewSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return [
            'frontpage_view',
            'about_view',
            'terms_and_conditions_view',
            'privacy_policy_view'
        ]

    def location(self, item):
        return reverse(item)


class MainCategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return MainCategory.objects.all()


class SubCategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return SubCategory.objects.all()
