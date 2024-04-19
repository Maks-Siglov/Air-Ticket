from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from booking_management.models.base import Base


class Booking(Base):
    __tablename__ = "booking_booking"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    flight_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("flight_flight.id", ondelete="CASCADE")
    )
    cart_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ticket_cart.id", ondelete="CASCADE")
    )
    ticket_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("ticket.id", ondelete="CASCADE"), nullable=True
    )
    booked_seat_number: Mapped[int]
    is_ordered: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now
    )

    flight = relationship("Flight", backref="bookings")
