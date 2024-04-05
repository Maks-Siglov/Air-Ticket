import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.dev")

app = Celery("air_ticket")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_RESULT_BACKEND

app.conf.redbeat_redis_url = settings.REDBEAT_REDIS_URL

app.conf.task_send_sent_event = True


app.autodiscover_tasks()
