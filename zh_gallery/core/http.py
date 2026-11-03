"""HTTP-утилиты."""

from __future__ import annotations

import ipaddress

from django.http import HttpRequest


def client_ip(request: HttpRequest) -> str | None:
    """IP клиента с учётом X-Forwarded-For от nginx.

    Значение проверяется как IP-адрес: в заголовок может прийти что угодно,
    а в модель согласия попадать мусор не должен.
    """
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR", "")
    candidate = forwarded.split(",")[0].strip() if forwarded else ""
    candidate = candidate or request.META.get("REMOTE_ADDR", "")
    try:
        return str(ipaddress.ip_address(candidate))
    except ValueError:
        return None
