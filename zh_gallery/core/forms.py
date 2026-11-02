"""Формы галереи."""

from __future__ import annotations

from django import forms
from django.utils.translation import gettext_lazy as _


class ReviewForm(forms.Form):
    """Новый комментарий к медиа-элементу."""

    content = forms.CharField(
        label=_("Leave the comment"),
        max_length=5000,
        strip=True,
        widget=forms.Textarea(attrs={"class": "textarea", "rows": 3}),
        error_messages={"required": _("Comment cannot be empty")},
    )
