from celery import Celery
from celery.schedules import crontab

from booking_management.core.settings import (
    CELERY_BROKER_URL,
    DEACTIVATE_BOOKING_MINUTE_SCHEDULE,
    REDBEAT_REDIS_URL,
)

app = Celery("booking_management")


app.conf.broker_url = CELERY_BROKER_URL
app.conf.result_backend = CELERY_BROKER_URL

app.conf.redbeat_redis_url = REDBEAT_REDIS_URL

app.conf.task_send_sent_event = True

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "delete_expired_bookings": {
        "task": "booking_management.task.deactivate_booking",
        "schedule": crontab(minute=f"*/{DEACTIVATE_BOOKING_MINUTE_SCHEDULE}"),
    }
}
