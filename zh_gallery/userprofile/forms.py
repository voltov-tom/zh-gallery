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
from django.conf import settings
from django.forms import CheckboxInput, Select, Textarea
from django.utils.translation import gettext_lazy as _

from core.http import client_ip

from .fields import CustomCharField
from .models import PersonalDataConsent


class BulmaFormMixin:
    """Добавляет CSS-класс Bulma ко всем полям формы.

    Класс зависит от типа виджета: чекбокс «запомнить меня» с классом ``input``
    превращался в пустое текстовое поле на всю ширину.
    """

    def widget_class_for(self, widget) -> str:
        if isinstance(widget, CheckboxInput):
            return "checkbox"
        if isinstance(widget, Select):
            return "select"
        if isinstance(widget, Textarea):
            return "textarea"
        return "input"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            classes = field.widget.attrs.get("class", "")
            widget_class = self.widget_class_for(field.widget)
            if widget_class not in classes.split():
                field.widget.attrs["class"] = f"{classes} {widget_class}".strip()


class LoginFormAllAuth(BulmaFormMixin, LoginForm):
    """Логин: у allauth поле называется «Login», подписываем понятнее."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "login" in self.fields:
            self.fields["login"].label = _("Username or e-mail")


class SignupFormAllAuth(BulmaFormMixin, SignupForm):
    """Регистрация: логин латиницей и обязательное согласие на обработку ПДн."""

    username = CustomCharField(
        label=_("Username"),
        min_length=app_settings.USERNAME_MIN_LENGTH,
        widget=forms.TextInput(attrs={"placeholder": _("Username"), "autocomplete": "username"}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # allauth собирает self.fields заново из ACCOUNT_SIGNUP_FIELDS,
        # поэтому поле, объявленное в классе, теряется — добавляем после super()
        self.fields["consent"] = forms.BooleanField(
            label=_("I agree to the processing of personal data"),
            required=True,
            error_messages={"required": _("Without consent we cannot create an account")},
            widget=forms.CheckboxInput(attrs={"class": "checkbox"}),
        )

    def save(self, request):
        user = super().save(request)
        PersonalDataConsent.objects.create(
            user=user,
            policy_version=settings.PRIVACY_POLICY_VERSION,
            ip_address=client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:255],
        )
        return user


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
