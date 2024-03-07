from datetime import datetime, timedelta

from django.db.models import Count, F, Q, QuerySet
from django.utils import timezone

from flight.models import Airplane, Flight, Seat
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

    flights = flights.annotate(
        airplane_economy_seats=Count(
            "airplane__seats__type",
            filter=Q(
                airplane__seats__type="Economy",
                airplane__seats__is_available=True,
            ),
        ),
        airplane_business_seats=Count(
            "airplane__seats__type",
            filter=Q(
                airplane__seats__type="Business",
                airplane__seats__is_available=True,
            ),
        ),
        airplane_first_class_seats=Count(
            "airplane__seats__type",
            filter=Q(
                airplane__seats__type="First Class",
                airplane__seats__is_available=True,
            ),
        ),
        airplane_total_seats=(
            F("airplane_economy_seats")
            + F("airplane_business_seats")
            + F("airplane_first_class_seats")
        ),
    )

    return flights


def get_flight_with_seats(flight_pk: int) -> Flight:
    return (
        Flight.objects.select_related(
            "airplane", "departure_airport", "arrival_airport"
        )
        .annotate(
            airplane_economy_seats=Count(
                "airplane__seats__type",
                filter=Q(
                    airplane__seats__type="Economy",
                    airplane__seats__is_available=True,
                ),
            ),
            airplane_business_seats=Count(
                "airplane__seats__type",
                filter=Q(
                    airplane__seats__type="Business",
                    airplane__seats__is_available=True,
                ),
            ),
            airplane_first_class_seats=Count(
                "airplane__seats__type",
                filter=Q(
                    airplane__seats__type="First Class",
                    airplane__seats__is_available=True,
                ),
            ),
        )
        .get(pk=flight_pk)
    )


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

    if status == "Future":
        flights = Flight.objects.filter(
            departure_scheduled__gte=timezone.now()
        )
    elif status == "Past":
        flights = Flight.objects.filter(
            departure_scheduled__lte=timezone.now()
        )
    else:
        flights = Flight.objects.all()

    return flights.select_related(
        "airplane", "departure_airport", "arrival_airport"
    )
