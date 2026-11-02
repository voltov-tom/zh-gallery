"""Контекст, доступный во всех шаблонах."""

from __future__ import annotations

from django.http import HttpRequest

from . import selectors

# URL-имена django-allauth: вход, регистрация, пароли, письма, соцаккаунты
_AUTH_URL_PREFIXES = ("account_", "socialaccount_", "mfa_", "usersessions_")
# ...но наши страницы профиля тоже начинаются с account_ — это не формы входа
_PROFILE_URL_NAMES = {"account_view", "my_account_view"}


def is_auth_page(request: HttpRequest) -> bool:
    """True для страниц входа/регистрации — на них включается отдельная тема."""
    match = getattr(request, "resolver_match", None)
    url_name = getattr(match, "url_name", "") or ""
    if url_name in _PROFILE_URL_NAMES:
        return False
    return url_name.startswith(_AUTH_URL_PREFIXES)


def site_context(request: HttpRequest) -> dict:
    return {
        "categories": selectors.get_categories(),
        "about": selectors.get_about(),
        "is_auth_page": is_auth_page(request),
    }
