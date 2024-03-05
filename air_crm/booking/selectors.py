from django.db.models import Count, Q

from booking.models import Ticket
from customer.models.contact import Contact
from flight.models import Airplane, Flight, Seat
from orders.models import Order


def get_flight(flight_pk: int) -> Flight:
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


def get_seat(airplane: Airplane, seat_type: str) -> Seat:
    seat = Seat.objects.filter(
        airplane=airplane, type=seat_type.title(), is_available=True
    ).first()
    return seat


def get_ticket(ticket_pk: int) -> Ticket:
    return Ticket.objects.select_related("passenger", "seat").get(pk=ticket_pk)


def get_contact(order: Order) -> Contact:
    return Contact.objects.filter(order=order).first()
