"""Модели приложения.

Своих «профильных» полей у пользователя нет — используется стандартный
``auth.User``. Здесь только юридически значимая запись: факт согласия на
обработку персональных данных (статья 9 152-ФЗ).
"""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class PersonalDataConsent(models.Model):
    """Согласие пользователя на обработку персональных данных.

    Храним дату, версию политики и IP — это позволяет подтвердить, что согласие
    было получено и на какой редакции документа.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name=_("user"),
        related_name="personal_data_consent",
        on_delete=models.CASCADE,
    )
    granted_at = models.DateTimeField(_("granted at"), default=timezone.now, db_index=True)
    policy_version = models.CharField(_("policy version"), max_length=32)
    ip_address = models.GenericIPAddressField(_("IP address"), null=True, blank=True)
    user_agent = models.CharField(_("user agent"), max_length=255, blank=True, default="")

    class Meta:
        verbose_name = _("personal data consent")
        verbose_name_plural = _("personal data consents")
        ordering = ["-granted_at"]

    def __str__(self) -> str:
        return f"{self.user} — {self.granted_at:%d.%m.%Y}"
