from django import forms
from django.utils.translation import gettext_lazy as _

from allauth.account.forms import LoginForm, SignupForm, AddEmailForm, ChangePasswordForm, SetPasswordForm, \
    ResetPasswordForm, ResetPasswordKeyForm
from allauth.account import app_settings

from .fields import CustomCharField


class LoginFormAllAuth(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs['class'] = 'input '
        self.fields['password'].widget.attrs['class'] = 'input '


class SignupFormAllAuth(SignupForm):
    username = CustomCharField(
        label=_("Username"),
        min_length=app_settings.USERNAME_MIN_LENGTH,
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Username"),
                "autocomplete": "username",
            },
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'input'
            })


class AddEmailFormAllAuth(AddEmailForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'input '
            })


class ChangePasswordFormAllAuth(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'input '
            })


class SetPasswordFormAllAuth(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'input '
            })


class ResetPasswordFormAllAuth(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'input '
            })


class ResetPasswordKeyFormAllAuth(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'input '
            })
