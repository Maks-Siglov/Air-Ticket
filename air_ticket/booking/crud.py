from datetime import datetime
from decimal import Decimal

from django.db.models import QuerySet, Sum

from booking.models import Booking, Ticket, TicketCart
from orders.models import Order, OrderTicket


def get_ticket(ticket_pk: int) -> Ticket | None:
    return (
        Ticket.objects.select_related("passenger").filter(pk=ticket_pk).first()
    )


def get_cart(cart_pk: int) -> TicketCart | None:
    return TicketCart.objects.filter(pk=cart_pk).first()


def get_cart_with_flight(cart_pk: int) -> TicketCart | None:
    return (
        TicketCart.objects.select_related("flight").filter(pk=cart_pk).first()
    )


def get_cart_with_flight_data(cart_pk: int) -> TicketCart | None:
    return (
        TicketCart.objects.select_related(
            "flight",
            "flight__airplane",
            "flight__departure_airport",
            "flight__arrival_airport",
        )
        .filter(pk=cart_pk)
        .first()
    )


def get_cart_tickets(cart: TicketCart) -> QuerySet[Ticket]:
    return Ticket.objects.filter(cart=cart).select_related("passenger")


def get_cart_total_price(cart: TicketCart) -> Decimal | None:
    return Ticket.objects.filter(cart=cart).aggregate(
        total_price=Sum("price")
    )["total_price"]


def get_first_booking(cart: TicketCart) -> Booking | None:
    return Booking.objects.filter(cart=cart, ticket=None).first()


def order_update_booking(order: Order) -> None:
    order_tickets_ids = list(
        OrderTicket.objects.filter(order=order).values_list(
            "ticket__id", flat=True
        )
    )
    Booking.objects.filter(ticket__id__in=order_tickets_ids).update(
        is_ordered=True
    )


def get_cart_with_contact(cart_pk: int) -> TicketCart | None:
    return (
        TicketCart.objects.select_related("contact").filter(pk=cart_pk).first()
    )


def get_expired_bookings_with_flight(
    threshold_time: datetime,
) -> QuerySet[Booking]:
    return Booking.objects.filter(
        ticket=None, created_at__lte=threshold_time
    ).select_related("flight")
