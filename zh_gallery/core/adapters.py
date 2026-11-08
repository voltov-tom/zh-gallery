"""Адаптер django-allauth.

Проект использует только HTML-письма (шаблоны ``*_message.html`` и
``*_subject.html``), поэтому стандартный адаптер, который ищет ``*.txt``,
падал бы с TemplateDoesNotExist при регистрации. Раньше этот класс лежал в
``core/utils.py`` и нигде не был подключён — то есть письма подтверждения
фактически не работали.
"""

from __future__ import annotations

from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string


class AccountAdapter(DefaultAccountAdapter):
    """Отправляет письма только в HTML и умеет закрывать регистрацию."""

    def is_open_for_signup(self, request):
        """SIGNUP_ENABLED=False закрывает и форму, и прямой заход на /accounts/signup/."""
        return bool(settings.SIGNUP_ENABLED) and super().is_open_for_signup(request)

    def render_mail(self, template_prefix, email, context, headers=None, **kwargs):
        recipients = [email] if isinstance(email, str) else email

        subject = render_to_string(f"{template_prefix}_subject.html", context)
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)

        body = render_to_string(
            f"{template_prefix}_message.html", context, request=self.request
        ).strip()
        if not body:
            raise TemplateDoesNotExist(f"{template_prefix}_message.html")

        message = EmailMultiAlternatives(
            subject,
            body,
            self.get_from_email(),
            recipients,
            headers=headers or {},
        )
        # Письмо без текстовой части: почтовые клиенты покажут HTML
        message.attach_alternative(body, "text/html")
        return message
