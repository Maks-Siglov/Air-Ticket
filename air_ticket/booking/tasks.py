from django.conf import settings

import requests
from celery import shared_task


@shared_task
def deactivate_expired_bookings() -> None:
    requests.post(
        f"http://{settings.DOMAIN_FOR_CELERY_TASKS}/api/v1/booking/"
        f"deactivate-expired-bookings/"
    )
