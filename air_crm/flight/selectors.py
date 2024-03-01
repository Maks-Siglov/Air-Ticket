from datetime import datetime, timedelta

from django.db.models import QuerySet, Q, Count, Sum, F

from flight.models import Flight


def get_searched_flights(
    departure_airport: str, destination_airport: str, departure_date: datetime
) -> QuerySet[Flight]:
    departure_date_min = departure_date - timedelta(days=3)
    departure_date_max = departure_date + timedelta(days=3)

    flights = Flight.objects.filter(
        Q(departure_airport=departure_airport) &
        Q(destination_airport=destination_airport) &
        Q(departure_date__range=(departure_date_min, departure_date_max))
    ).order_by('departure_date').select_related("airplane")

    flights = flights.annotate(
        airplane_economy_seats=Count(
            'airplane__seats__type',
            filter=Q(airplane__seats__type='Economy')
        ),
        airplane_business_seats=Count(
            'airplane__seats__type',
            filter=Q(airplane__seats__type='Business')
        ),
        airplane_first_class_seats=Count(
            'airplane__seats__type',
            filter=Q(airplane__seats__type='First Class')
        ),
        airplane_total_seats=(
                F('airplane_economy_seats') +
                F('airplane_business_seats') +
                F('airplane_first_class_seats')
        )
    )

    return flights
