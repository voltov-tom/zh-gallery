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
def social_apps(db):
    """Кнопки провайдеров рисуются, когда SocialApp настроен (как в живой БД)."""
    from allauth.socialaccount.models import SocialApp
    from django.contrib.sites.models import Site

    site = Site.objects.get(pk=settings.SITE_ID)
    apps = []
    for provider, name in (("vk", "VK"), ("mailru", "Mail.ru")):
        app = SocialApp.objects.create(
            provider=provider, name=name, client_id=f"{provider}-id", secret="test-secret"
        )
        app.sites.add(site)
        apps.append(app)
    return apps


@pytest.mark.django_db
def test_login_page_uses_local_provider_icons(client, social_apps):
    response = client.get(reverse("account_login"))
    content = response.content

    assert b"core/images/social/vk.svg" in content
    assert b"core/images/social/mailru.svg" in content
    assert b"upload.wikimedia.org" not in content
    # Google больше не подключён как провайдер входа
    assert b"socialaccount_provider google" not in content
    assert b"core/images/social/google.svg" not in content


def test_provider_button_has_russian_translation():
    """В тестах .mo не собирается (он в .gitignore) — проверяем сам каталог."""
    po = pathlib.Path(settings.BASE_DIR) / "locale/ru/LC_MESSAGES/django.po"

    content = po.read_text()
    assert 'msgid "Continue with %(provider_name)s"' in content
    assert 'msgstr "Продолжить с %(provider_name)s"' in content


def test_google_provider_is_not_installed():
    assert "allauth.socialaccount.providers.google" not in settings.INSTALLED_APPS
    assert "vk" in settings.SOCIALACCOUNT_PROVIDERS
    assert "mailru" in settings.SOCIALACCOUNT_PROVIDERS


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


@pytest.mark.django_db
def test_signup_can_be_closed_by_setting(client, settings):
    """SIGNUP_ENABLED=False: нет кнопки в шапке и прямой заход не открывает форму."""
    settings.SIGNUP_ENABLED = False

    page = client.get(reverse("account_login"))
    assert b"/accounts/signup/" not in page.content
    assert b"Registration is temporarily closed" in page.content

    response = client.get(reverse("account_signup"))
    assert response.status_code == 200
    assert b"temporarily closed" in response.content
    assert b'name="password1"' not in response.content


@pytest.mark.django_db
def test_signup_is_open_by_default(client):
    page = client.get(reverse("account_login"))

    assert b"/accounts/signup/" in page.content
