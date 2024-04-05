from datetime import datetime, timedelta

from django.db.models import F, Q, QuerySet
from django.utils import timezone

from booking.models import Booking
from flight.models import Airplane, Airport, Flight, Seat
from orders.models import Order
from users.models import User


def get_searched_flights(
    departure_airport: str, arrival_airport: str, departure_date: datetime
) -> QuerySet[Flight]:
    departure_date_min = departure_date - timedelta(days=3)
    departure_date_max = departure_date + timedelta(days=3)

    flights = (
        Flight.objects.filter(
            Q(departure_airport__name__icontains=departure_airport)
            & Q(arrival_airport__name__icontains=arrival_airport)
            & Q(
                departure_scheduled__range=(
                    departure_date_min,
                    departure_date_max,
                )
            )
        )
        .select_related("airplane", "departure_airport", "arrival_airport")
        .order_by("departure_scheduled")
    )
    booked_places = len(
        Booking.objects
        .filter(flight__in=flights)
    )

    flights = flights.annotate(
        available_seats=F("airplane__seats_amount") - booked_places
    )
    return flights


def get_flight_with_seats(flight_pk: int) -> Flight:
    return Flight.objects.select_related(
        "airplane", "departure_airport", "arrival_airport"
    ).get(pk=flight_pk)


def get_flight(flight_pk: int) -> Flight:
    return Flight.objects.select_related(
        "airplane", "departure_airport", "arrival_airport"
    ).get(pk=flight_pk)


def get_seat(airplane: Airplane, seat_type: str) -> Seat:
    seat = Seat.objects.filter(
        airplane=airplane, type=seat_type.title(), is_available=True
    ).first()
    return seat


def get_user_flights(user: User, status: str) -> QuerySet[Flight]:
    flight_ids = Order.objects.filter(user=user).values_list("flight_id")
    flights = Flight.objects.filter(id__in=flight_ids).order_by(
        "departure_scheduled"
    )
    if status == "Future":
        flights = flights.objects.filter(
            departure_scheduled__gte=timezone.now()
        )
    elif status == "Past":
        flights = flights.objects.filter(
            departure_scheduled__lte=timezone.now()
        )

    return flights.select_related(
        "airplane", "departure_airport", "arrival_airport"
    )


def get_suggestion_airports(value: str) -> QuerySet[Airport]:
    return Airport.objects.filter(name__icontains=value)[:10]
