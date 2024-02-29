from datetime import datetime, timedelta

from django.db.models import QuerySet, Q

from flight.models import Flight


def get_searched_flights(
    departure_airport: str, destination_airport: str, departure_date: datetime
) -> QuerySet[Flight]:
    departure_date_min = departure_date - timedelta(days=3)
    departure_date_max = departure_date + timedelta(days=3)

    return Flight.objects.filter(
        Q(departure_airport=departure_airport) &
        Q(destination_airport=destination_airport) &
        Q(departure_date__range=(departure_date_min, departure_date_max))
    )
