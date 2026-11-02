"""Тесты аутентификации: адаптер писем и формы allauth."""

from __future__ import annotations

import pytest
from allauth.account.adapter import get_adapter
from django.conf import settings
from django.urls import reverse

from core.adapters import AccountAdapter
from userprofile.forms import LoginFormAllAuth, SignupFormAllAuth


def test_custom_adapter_is_configured():
    assert settings.ACCOUNT_ADAPTER == "core.adapters.AccountAdapter"
    assert isinstance(get_adapter(), AccountAdapter)


def test_custom_forms_are_wired():
    assert settings.ACCOUNT_FORMS["login"] == "userprofile.forms.LoginFormAllAuth"
    assert settings.ACCOUNT_FORMS["signup"] == "userprofile.forms.SignupFormAllAuth"


@pytest.mark.django_db
def test_signup_sends_html_confirmation_email(client, mailoutbox):
    response = client.post(
        reverse("account_signup"),
        {
            "email": "new@example.com",
            "username": "newuser",
            "password1": "strong-password-777",
            "password2": "strong-password-777",
        },
    )

    assert response.status_code == 302
    assert len(mailoutbox) == 1
    message = mailoutbox[0]
    assert message.alternatives, "письмо должно содержать HTML-часть"
    html, mimetype = message.alternatives[0]
    assert mimetype == "text/html"
    assert "http" in html


@pytest.mark.django_db
def test_signup_form_rejects_cyrillic_username():
    form = SignupFormAllAuth(
        data={
            "email": "user@example.com",
            "username": "кириллица",
            "password1": "strong-password-777",
            "password2": "strong-password-777",
        }
    )

    assert not form.is_valid()
    assert "username" in form.errors


def test_login_form_has_bulma_classes():
    form = LoginFormAllAuth()

    assert "input" in form.fields["login"].widget.attrs["class"]
    assert "input" in form.fields["password"].widget.attrs["class"]
