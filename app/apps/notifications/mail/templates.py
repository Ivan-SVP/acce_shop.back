from django.utils.translation import gettext_lazy as _

from config import settings


class Templates:
    """Email templates for the services.mail.backend.TemplatesMailer"""

    @staticmethod
    def company_created(company_title):
        return {
            'subject': f'{_("Company created on")} "{settings.COMPANY_TITLE}"',
            'message': f'{_("Company")} {company_title} {_("created")}. '
                       f'{_("It will become available after verification")}'
        }
