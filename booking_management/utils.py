from datetime import datetime

from sqlalchemy import Sequence, and_, select
from sqlalchemy.orm import Session, selectinload

from models import Booking


def get_expired_bookings(
    session: Session, threshold_time: datetime
) -> Sequence[Booking]:
    query = (
        select(Booking)
        .options(selectinload(Booking.flight))
        .filter(
            and_(
                Booking.ticket_id == None,
                Booking.created_at <= threshold_time,
                Booking.is_active == True,
            )
        )
    )

    return session.scalars(query).all()
