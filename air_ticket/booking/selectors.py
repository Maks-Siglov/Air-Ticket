from decimal import Decimal

from django.db.models import QuerySet, Sum

from booking.models import Ticket, TicketCart, Booking
from orders.models import OrderTicket, Order


def get_ticket(ticket_pk: int) -> Ticket:
    return Ticket.objects.select_related("passenger").get(pk=ticket_pk)


def get_cart(cart_pk: int) -> TicketCart:
    return TicketCart.objects.get(pk=cart_pk)


def get_cart_with_flight(cart_pk: int) -> TicketCart:
    return TicketCart.objects.select_related("flight").get(pk=cart_pk)


def get_cart_tickets(cart: TicketCart) -> QuerySet[Ticket]:
    return Ticket.objects.filter(cart=cart).select_related("passenger")


def get_cart_total_price(cart: TicketCart) -> Decimal:
    return Ticket.objects.filter(cart=cart).aggregate(
        total_price=Sum("price")
    )["total_price"] or Decimal("0.00")


def get_first_booking(cart: TicketCart) -> Booking:
    return Booking.objects.filter(cart=cart, ticket=None).first()


def order_update_booking(order: Order) -> None:
    order_tickets_ids = list(
        OrderTicket.objects
        .filter(order=order)
        .values_list("ticket__id", flat=True)
    )
    Booking.objects.filter(ticket__id__in=order_tickets_ids).update(
        is_ordered=True
    )
