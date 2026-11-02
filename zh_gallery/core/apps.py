from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = _("Gallery")

    def ready(self) -> None:
        # подключает post_migrate-обработчик синхронизации Site
        from . import signals  # noqa: F401
