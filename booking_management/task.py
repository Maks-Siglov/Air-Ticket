from datetime import datetime, timedelta

from django.core.mail import EmailMultiAlternatives

import pytz
from celery import shared_task
from sqlalchemy import func

from booking_management.core import settings
from booking_management.crud import get_expired_bookings
from booking_management.db.main import get_session
from booking_management.models import Booking


@shared_task
def deactivate_booking():
    session = get_session()

    utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
    threshold_time = utc_now - timedelta(
        minutes=settings.BOOKING_MINUTES_LIFETIME
    )

    expired_bookings = get_expired_bookings(session, threshold_time)

    if not expired_bookings:
        return "There are no expired bookings"

    for booking in expired_bookings:
        flight = booking.flight
        seat_to_remove = booking.booked_seat_number

        updated_booked_seats = func.array_remove(
            flight.booked_seats, seat_to_remove
        )
        flight.booked_seats = updated_booked_seats

    session.query(Booking).filter(
        Booking.id.in_([booking.id for booking in expired_bookings])
    ).update({Booking.is_active: False}, synchronize_session=False)

    session.commit()
    return "Expired bookings have been deactivated."


@shared_task
def send_tickets_email(html_content: str, user_email: str) -> None:

    mail = EmailMultiAlternatives(
        subject="AirTicket",
        body=html_content,
        from_email="etqueens22@gmail.com",
        to=[user_email],
    )
    mail.attach_alternative(html_content, "text/html")

    mail.send()
