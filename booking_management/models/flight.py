from datetime import datetime

from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql.sqltypes import ARRAY

from booking_management.models.base import Base


class Flight(Base):
    __tablename__ = "flight_flight"

    id: Mapped[int] = mapped_column(primary_key=True)
    number: Mapped[str]
    iata: Mapped[str]
    icao: Mapped[str]
    price: Mapped[int] = mapped_column(Integer, default=120)
    lunch_price: Mapped[int] = mapped_column(Integer, default=15)
    luggage_price: Mapped[int] = mapped_column(Integer, default=50)
    airplane_id: Mapped[int]
    arrival_airport_id: Mapped[int]
    departure_airport_id: Mapped[int]
    arrival_scheduled: Mapped[datetime]
    departure_scheduled: Mapped[datetime]
    seats: Mapped[list] = mapped_column(ARRAY(Integer), nullable=True)
    booked_seats: Mapped[list] = mapped_column(ARRAY(Integer), nullable=True)
    ordered_seats: Mapped[list] = mapped_column(ARRAY(Integer), nullable=True)
