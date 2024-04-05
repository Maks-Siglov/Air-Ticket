import requests

from django.conf import settings
from celery import shared_task


@shared_task
def delete_expired_bookings() -> None:
    requests.post(
        f"http://{settings.DOMAIN_FOR_CELERY_TASKS}/api/v1/booking/"
        f"delete-expired-bookings/"
    )
