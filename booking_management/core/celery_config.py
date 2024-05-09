from celery import Celery
from celery.schedules import crontab

from booking_management.core import settings
from booking_management.task import deactivate_booking

app = Celery("booking_management")


app.conf.broker_url = settings.CELERY_BROKER_URL
app.conf.result_backend = settings.CELERY_BROKER_URL

app.conf.redbeat_redis_url = settings.REDBEAT_REDIS_URL

app.conf.task_send_sent_event = True

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "delete_expired_bookings": {
        "task": "booking_management.task.deactivate_booking",
        "schedule": crontab(
            minute=f"*/{settings.DEACTIVATE_BOOKING_MINUTE_SCHEDULE}"
        ),
    }
}
