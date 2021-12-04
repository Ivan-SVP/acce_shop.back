import os
from celery import Celery
from kombu import Queue, Exchange

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

celery_app = Celery('config')
celery_app.config_from_object('django.conf:settings')
celery_app.autodiscover_tasks()

celery_app.conf.task_time_limit = 60*60*24
celery_app.conf.task_soft_time_limit = 60*60*24

celery_app.conf.task_default_queue = 'default'
celery_app.conf.task_queues = (
    Queue('default', Exchange('default'),  routing_key='default'),
    Queue('mail', Exchange('mail'), routing_key='mail'),
)

celery_app.conf.task_routes = {
    'services.mail.tasks*': {
        'queue': 'mail',
        'priority': 5,
    },
}
