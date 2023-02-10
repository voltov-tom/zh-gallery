from django.forms import CharField
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class CustomCharField(CharField):
    """custom char field to validate not latin usernames"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validators.append(
            RegexValidator(regex='^[a-zA-Z0-9]*$', message=_('Username must be Alphanumeric'), code='invalid_username')
        )
