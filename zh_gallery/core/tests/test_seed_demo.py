"""Тест демо-команды: данные создаются, демо-пользователь может войти."""

from __future__ import annotations

import pytest
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.core.management import call_command

from core.models import About, MainCategory, MediaItem


@pytest.mark.django_db
def test_seed_demo_creates_content_and_verified_user():
    call_command("seed_demo", verbosity=0)

    assert MainCategory.objects.count() == 2
    assert MediaItem.objects.count() == 9
    assert About.objects.count() == 1

    user = get_user_model().objects.get(username="demo")
    assert EmailAddress.objects.filter(user=user, email=user.email, verified=True).exists()


@pytest.mark.django_db
def test_seed_demo_is_idempotent():
    call_command("seed_demo", verbosity=0)
    call_command("seed_demo", verbosity=0)

    assert MediaItem.objects.count() == 9
    assert MainCategory.objects.count() == 2


@pytest.mark.django_db
def test_seeded_user_can_log_in(client):
    call_command("seed_demo", verbosity=0)

    assert client.login(username="demo", password="demo-password-12345")


@pytest.mark.django_db
def test_reset_removes_previous_content():
    call_command("seed_demo", verbosity=0)

    call_command("seed_demo", "--reset", verbosity=0)

    assert MainCategory.objects.count() == 2
    assert MediaItem.objects.count() == 9
