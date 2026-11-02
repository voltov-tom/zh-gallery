"""Формы django-allauth в стиле Bulma.

Все кастомные формы приводили один и тот же список полей к классу ``input``;
вместо семи копий — один миксин.
"""

from __future__ import annotations

from allauth.account import app_settings
from allauth.account.forms import (
    AddEmailForm,
    ChangePasswordForm,
    LoginForm,
    ResetPasswordForm,
    ResetPasswordKeyForm,
    SetPasswordForm,
    SignupForm,
)
from django import forms
from django.utils.translation import gettext_lazy as _

from .fields import CustomCharField


class BulmaFormMixin:
    """Добавляет CSS-класс Bulma ко всем полям формы."""

    widget_class = "input"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            classes = field.widget.attrs.get("class", "")
            if self.widget_class not in classes.split():
                field.widget.attrs["class"] = f"{classes} {self.widget_class}".strip()


class LoginFormAllAuth(BulmaFormMixin, LoginForm):
    pass


class SignupFormAllAuth(BulmaFormMixin, SignupForm):
    """Регистрация с проверкой логина на латиницу/цифры."""

    username = CustomCharField(
        label=_("Username"),
        min_length=app_settings.USERNAME_MIN_LENGTH,
        widget=forms.TextInput(attrs={"placeholder": _("Username"), "autocomplete": "username"}),
    )


class AddEmailFormAllAuth(BulmaFormMixin, AddEmailForm):
    pass


class ChangePasswordFormAllAuth(BulmaFormMixin, ChangePasswordForm):
    pass


class SetPasswordFormAllAuth(BulmaFormMixin, SetPasswordForm):
    pass


class ResetPasswordFormAllAuth(BulmaFormMixin, ResetPasswordForm):
    pass


class ResetPasswordKeyFormAllAuth(BulmaFormMixin, ResetPasswordKeyForm):
    pass
