"""Контекст, доступный во всех шаблонах."""

from __future__ import annotations

from django.conf import settings
from django.http import HttpRequest

from . import selectors

# URL-имена django-allauth: вход, регистрация, пароли, письма, соцаккаунты
_AUTH_URL_PREFIXES = ("account_", "socialaccount_", "mfa_", "usersessions_")
# ...но наши страницы профиля тоже начинаются с account_ — это не формы входа
_PROFILE_URL_NAMES = {"account_view", "my_account_view"}


def is_auth_page(request: HttpRequest) -> bool:
    """True для страниц входа/регистрации — на них включается отдельная тема.

    Часть маршрутов allauth не попадает под префиксы: вход через провайдера
    называется ``google_login``, ``vk_login`` и т. п. Поэтому как признак
    используем ещё и префикс пути: всё под /accounts/ — это страницы аккаунта,
    кроме наших профилей.
    """
    match = getattr(request, "resolver_match", None)
    url_name = getattr(match, "url_name", "") or ""
    if url_name in _PROFILE_URL_NAMES:
        return False
    if url_name.startswith(_AUTH_URL_PREFIXES):
        return True
    return request.path.startswith("/accounts/")


def site_context(request: HttpRequest) -> dict:
    return {
        "categories": selectors.get_categories(),
        "about": selectors.get_about(),
        "is_auth_page": is_auth_page(request),
        "policy_version": settings.PRIVACY_POLICY_VERSION,
        "signup_enabled": settings.SIGNUP_ENABLED,
    }
