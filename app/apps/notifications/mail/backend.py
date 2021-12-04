import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core import mail as default_django_mailer

from apps.notifications.mail.templates import Templates


logger = logging.getLogger(__name__)
User = get_user_model()


class TemplatesMailer:
    def __init__(self, fail_silently=False, from_email=settings.DEFAULT_FROM_EMAIL):
        self.Mailer = default_django_mailer

        self.fail_silently = fail_silently
        self.from_email = from_email

        self.sending_args = []
        self.sending_kwargs = {}
        self.template_name = ''

    def send(self, template_name: str, recipient_list, *args, **kwargs):
        self.sending_kwargs = kwargs
        self.sending_args = args
        self.template_name = template_name

        sending_data = self._get_sending_data(recipient_list)
        self.Mailer.send_mail(**sending_data)

    def _get_sending_data(self, recipient_list) -> dict:
        template_data = self._get_template_data()

        template_data['from_email'] = self.from_email,
        template_data['recipient_list'] = recipient_list,
        template_data['fail_silently'] = self.fail_silently,

        return template_data

    def _get_template_data(self) -> dict:
        return self.template_method(*self.sending_args, **self.sending_kwargs)

    @property
    def template_method(self):
        return getattr(Templates, self.template_name)
