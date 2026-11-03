"""Тесты аутентификации: адаптер писем и формы allauth."""

from __future__ import annotations

import pathlib

import pytest
from allauth.account.adapter import get_adapter
from django.conf import settings
from django.contrib.auth import get_user_model
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
            "consent": "on",
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
            "consent": "on",
        }
    )

    assert not form.is_valid()
    assert "username" in form.errors


def test_login_form_has_bulma_classes():
    form = LoginFormAllAuth()

    assert "input" in form.fields["login"].widget.attrs["class"]
    assert "input" in form.fields["password"].widget.attrs["class"]


@pytest.mark.django_db
def test_login_page_has_auth_theme(client):
    response = client.get(reverse("account_login"))

    assert response.status_code == 200
    assert b'class="auth-page"' in response.content
    assert b"core/css/auth.css" in response.content


@pytest.mark.django_db
def test_profile_page_is_not_styled_as_auth_page(client, user):
    response = client.get(reverse("account_view", args=[user.username]))

    assert b'class="auth-page"' not in response.content


@pytest.mark.django_db
def test_remember_me_renders_as_checkbox(client):
    """Раньше чекбоксу доставался класс `input`, и он выглядел как пустое поле."""
    response = client.get(reverse("account_login"))
    form = response.context["form"]

    assert form.fields["remember"].widget.attrs["class"].split() == ["checkbox"]
    assert b'type="checkbox"' in response.content


@pytest.fixture
def google_social_app(db):
    """Кнопка провайдера рисуется только когда SocialApp настроен (как в живой БД)."""
    from allauth.socialaccount.models import SocialApp
    from django.contrib.sites.models import Site

    app = SocialApp.objects.create(
        provider="google", name="Google", client_id="test-id", secret="test-secret"
    )
    app.sites.add(Site.objects.get(pk=settings.SITE_ID))
    return app


@pytest.mark.django_db
def test_login_page_uses_local_google_icon(client, google_social_app):
    response = client.get(reverse("account_login"))

    assert b"core/images/social/google.svg" in response.content
    assert b"upload.wikimedia.org" not in response.content


def test_google_button_has_russian_translation():
    """В тестах .mo не собирается (он в .gitignore) — проверяем сам каталог."""
    po = pathlib.Path(settings.BASE_DIR) / "locale/ru/LC_MESSAGES/django.po"

    content = po.read_text()
    assert 'msgid "Continue with Google"' in content
    assert 'msgstr "Продолжить с Google"' in content


@pytest.mark.django_db
def test_signup_requires_personal_data_consent(client):
    """Без согласия на обработку ПДн (ст. 9 152-ФЗ) аккаунт не создаётся."""
    response = client.post(
        reverse("account_signup"),
        {
            "email": "no-consent@example.com",
            "username": "noconsent",
            "password1": "strong-password-777",
            "password2": "strong-password-777",
        },
    )

    assert response.status_code == 200
    assert get_user_model().objects.filter(username="noconsent").exists() is False
    assert b"consent" in response.content


@pytest.mark.django_db
def test_signup_stores_consent_record(client, settings):
    settings.PRIVACY_POLICY_VERSION = "2026-11-02"

    client.post(
        reverse("account_signup"),
        {
            "email": "consented@example.com",
            "username": "consented",
            "password1": "strong-password-777",
            "password2": "strong-password-777",
            "consent": "on",
        },
    )

    from userprofile.models import PersonalDataConsent

    consent = PersonalDataConsent.objects.get(user__username="consented")
    assert consent.policy_version == "2026-11-02"
    assert consent.ip_address == "127.0.0.1"
    assert consent.granted_at is not None


@pytest.mark.django_db
def test_signup_page_mentions_privacy_policy(client):
    response = client.get(reverse("account_signup"))
    content = response.content

    assert b"auth-checkbox--consent" in content
    assert b"privacy-policy" in content


@pytest.mark.django_db
def test_consent_is_shown_in_account(client, user):
    from userprofile.models import PersonalDataConsent

    PersonalDataConsent.objects.create(user=user, policy_version="2026-11-02")
    client.force_login(user)

    response = client.get(reverse("my_account_view"))

    assert b"profile-consent" in response.content


@pytest.mark.django_db
def test_cookie_notice_is_on_pages(client):
    content = client.get(reverse("frontpage_view")).content

    assert b"data-cookie-notice" in content
    assert b"core/js/cookie.js" in content
    assert b"privacy-policy" in content
