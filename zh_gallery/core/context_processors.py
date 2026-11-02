"""Контекст, доступный во всех шаблонах."""

from __future__ import annotations

from django.http import HttpRequest

from . import selectors


def site_context(request: HttpRequest) -> dict:
    return {
        "categories": selectors.get_categories(),
        "about": selectors.get_about(),
    }
