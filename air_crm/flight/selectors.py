from datetime import datetime, timedelta

from django.db.models import QuerySet, Q, Count, F

from flight.models import Flight


def get_searched_flights(
    departure_airport: str, arrival_airport: str, departure_date: datetime
) -> QuerySet[Flight]:
    departure_date_min = departure_date - timedelta(days=3)
    departure_date_max = departure_date + timedelta(days=3)

    flights = (
        Flight.objects.filter(
            Q(departure__airport=departure_airport)
            & Q(arrival__airport=arrival_airport)
            & Q(
                departure__scheduled__range=(
                    departure_date_min,
                    departure_date_max,
                )
            )
        )
        .order_by("departure__scheduled")
        .select_related("airplane")
    )

    flights = flights.annotate(
        airplane_economy_seats=Count(
            "airplane__seats__type", filter=Q(airplane__seats__type="Economy")
        ),
        airplane_business_seats=Count(
            "airplane__seats__type", filter=Q(airplane__seats__type="Business")
        ),
        airplane_first_class_seats=Count(
            "airplane__seats__type",
            filter=Q(airplane__seats__type="First Class"),
        ),
        airplane_total_seats=(
            F("airplane_economy_seats")
            + F("airplane_business_seats")
            + F("airplane_first_class_seats")
        ),
    )

    return flights
