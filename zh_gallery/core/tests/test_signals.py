"""Тесты синхронизации django.contrib.sites с настройками."""

from __future__ import annotations

import types

import pytest
from django.contrib.sites.models import Site

from core.signals import sync_site_from_settings

SITES_APP = types.SimpleNamespace(name="django.contrib.sites", label="sites")
CORE_APP = types.SimpleNamespace(name="core", label="core")


@pytest.mark.django_db
def test_site_is_updated_from_settings(settings):
    settings.SITE_DOMAIN = "gallery.test"
    settings.SITE_NAME = "Gallery"
    Site.objects.update_or_create(
        pk=settings.SITE_ID, defaults={"domain": "example.com", "name": "example.com"}
    )

    sync_site_from_settings(sender=SITES_APP, app_config=SITES_APP)

    site = Site.objects.get(pk=settings.SITE_ID)
    assert site.domain == "gallery.test"
    assert site.name == "Gallery"


@pytest.mark.django_db
def test_site_is_ignored_for_other_apps(settings):
    settings.SITE_DOMAIN = "gallery.test"
    Site.objects.update_or_create(
        pk=settings.SITE_ID, defaults={"domain": "example.com", "name": "example.com"}
    )

    sync_site_from_settings(sender=CORE_APP, app_config=CORE_APP)

    assert Site.objects.get(pk=settings.SITE_ID).domain == "example.com"


@pytest.mark.django_db
def test_empty_domain_keeps_existing_site(settings):
    settings.SITE_DOMAIN = ""
    Site.objects.update_or_create(
        pk=settings.SITE_ID, defaults={"domain": "example.com", "name": "example.com"}
    )

    sync_site_from_settings(sender=SITES_APP, app_config=SITES_APP)

    assert Site.objects.get(pk=settings.SITE_ID).domain == "example.com"
