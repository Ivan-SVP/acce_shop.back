import logging

from config.celery import celery_app
from apps.notifications.mail.backend import TemplatesMailer


logger = logging.getLogger(__name__)


@celery_app.task
def send_templated_email(template_name, recipient_list, *args, **kwargs):
    try:
        TemplatesMailer().send(template_name, recipient_list, *args, **kwargs)
    except Exception as ex:
        logger.exception(ex)
