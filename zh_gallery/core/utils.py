from allauth.account.adapter import DefaultAccountAdapter

from django.core.mail import EmailMultiAlternatives
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string


class DefaultAccountAdapterCustom(DefaultAccountAdapter):
    """
    overwrite 'render_mail' to send only 'html' e-mails
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def render_mail(self, template_prefix, email, context):
        to = [email] if isinstance(email, str) else email
        subject = render_to_string("{0}_subject.html".format(template_prefix), context)
        subject = " ".join(subject.splitlines()).strip()
        subject = self.format_email_subject(subject)

        from_email = self.get_from_email()

        body = ''

        try:
            template_name = f"{template_prefix}_message.html"
            body = render_to_string(
                template_name,
                context,
                self.request,
            ).strip()
        except TemplateDoesNotExist:
            if not body:
                raise

        msg = EmailMultiAlternatives(subject, body, from_email, to)
        msg.attach_alternative(body, "text/html")
        return msg
