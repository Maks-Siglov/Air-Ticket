from datetime import datetime, timedelta

from django.db.models import Count, F, Q, QuerySet

from flight.models import Flight


def get_searched_flights(
    departure_airport: str, arrival_airport: str, departure_date: datetime
) -> QuerySet[Flight]:
    departure_date_min = departure_date - timedelta(days=3)
    departure_date_max = departure_date + timedelta(days=3)

    flights = (
        Flight.objects.filter(
            Q(departure_airport__name=departure_airport)
            & Q(arrival_airport__name=arrival_airport)
            & Q(
                departure_scheduled__range=(
                    departure_date_min,
                    departure_date_max,
                )
            )
        )
        .order_by("departure_scheduled")
        .select_related("airplane", "departure_airport", "arrival_airport")
    )

    flights = flights.annotate(
        airplane_economy_seats=Count(
            "airplane__seats__type", filter=Q(
                airplane__seats__type="Economy",
                airplane__seats__is_available=True
            )
        ),
        airplane_business_seats=Count(
            "airplane__seats__type", filter=Q(
                airplane__seats__type="Business",
                airplane__seats__is_available=True
            )
        ),
        airplane_first_class_seats=Count(
            "airplane__seats__type",
            filter=Q(
                airplane__seats__type="First Class",
                airplane__seats__is_available=True
            ),
        ),
        airplane_total_seats=(
            F("airplane_economy_seats")
            + F("airplane_business_seats")
            + F("airplane_first_class_seats")
        ),
    )

    return flights
