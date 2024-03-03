from django.db.models import Count, QuerySet, Q

from flight.models import Airplane, Flight, Seat


def get_flight(flight_pk: int) -> Flight:
    return (
        Flight.objects
        .select_related("airplane", "departure", "arrival")
        .annotate(
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
            )
        )
        .get(pk=flight_pk)
    )


def get_seat(airplane: Airplane, seat_type: str) -> Seat:
    seat = Seat.objects.filter(
        airplane=airplane, type=seat_type.capitalize(), is_available=True
    ).first()
    seat.is_available = False
    seat.save()
    return seat
