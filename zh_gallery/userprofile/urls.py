"""Маршруты личного кабинета.

``<str:>`` вместо ``<slug:>``: slug-конвертер не принимает точки и подчёркивания,
а логины в allauth ими не ограничены — личный кабинет такого пользователя
просто не открывался.
"""

from __future__ import annotations

from django.urls import path

from .views import AccountView, MyAccountView

urlpatterns = [
    path("accounts/my-account/", MyAccountView.as_view(), name="my_account_view"),
    path("accounts/<str:user_name>/", AccountView.as_view(), name="account_view"),
]
