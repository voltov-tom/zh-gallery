"""Админка: журнал согласий на обработку персональных данных.

Сам пользователь управляется стандартной админкой ``django.contrib.auth``,
а сущности галереи зарегистрированы в ``core/admin.py``.
"""

from __future__ import annotations

from django.contrib import admin

from .models import PersonalDataConsent


@admin.register(PersonalDataConsent)
class PersonalDataConsentAdmin(admin.ModelAdmin):
    list_display = ("user", "granted_at", "policy_version", "ip_address")
    list_filter = ("policy_version", "granted_at")
    search_fields = ("user__username", "user__email", "ip_address")
    autocomplete_fields = ("user",)
    readonly_fields = ("user", "granted_at", "policy_version", "ip_address", "user_agent")

    def has_add_permission(self, request) -> bool:
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False
