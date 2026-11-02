"""Кастомные поля форм."""

from __future__ import annotations

from django import forms
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class CustomCharField(forms.CharField):
    """Логин только из латиницы и цифр (кириллица в username не допускается)."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(
            RegexValidator(
                regex=r"^[a-zA-Z0-9]+$",
                message=_("Username must be Alphanumeric"),
                code="invalid_username",
            )
        )
