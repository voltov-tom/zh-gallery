"""Сигналы приложения core.

Единственный сценарий: после миграций привести объект ``django.contrib.sites``
к домену из настроек. Без этого allauth строил абсолютные ссылки в письмах от
``example.com``: на свежей базе Site #1 никто не заполняет, и подтверждение
почты ведёт на несуществующий хост.
"""

from __future__ import annotations

import logging

from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver

logger = logging.getLogger(__name__)


@receiver(post_migrate, dispatch_uid="core.sync_site_from_settings")
def sync_site_from_settings(sender, app_config=None, **kwargs) -> None:
    """Вызывается Django после migrate — по одному разу на каждое приложение."""
    # AppConfig.name — это "django.contrib.sites", а короткое имя — label
    if getattr(app_config, "label", None) != "sites":
        return

    domain = getattr(settings, "SITE_DOMAIN", "")
    if not domain:
        return

    from django.contrib.sites.models import Site

    site, created = Site.objects.update_or_create(
        pk=settings.SITE_ID,
        defaults={"domain": domain, "name": getattr(settings, "SITE_NAME", domain)},
    )
    logger.info("Site #%s %s: %s", site.pk, "создан" if created else "обновлён", site.domain)
