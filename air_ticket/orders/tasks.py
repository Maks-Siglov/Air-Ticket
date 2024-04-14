from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from celery import shared_task


@shared_task
def send_tickets_email(html_content: str, user_email: str) -> None:

    mail = EmailMultiAlternatives(
        subject="AirTicket",
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user_email],
    )
    mail.attach_alternative(html_content, "text/html")

    mail.send()
