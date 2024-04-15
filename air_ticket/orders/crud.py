from django.db.models import QuerySet

from flight.models import Seat
from orders.models import Order
from orders.models.order_ticket import OrderTicket
from users.models import User


def get_order(order_pk: int) -> Order:
    return Order.objects.get(pk=order_pk)


def get_order_with_flight(order_pk: int) -> Order | None:
    return (
        Order.objects.select_related(
            "flight",
            "flight__airplane",
            "flight__departure_airport",
            "flight__arrival_airport",
        )
        .filter(pk=order_pk)
        .first()
    )


def get_user_orders(user: User) -> QuerySet[Order]:
    return (
        Order.objects.filter(user=user)
        .select_related("flight__departure_airport", "flight__arrival_airport")
        .order_by("created_at")
    )


def get_passenger_order_tickets(order: Order) -> QuerySet[OrderTicket]:
    return OrderTicket.objects.filter(order=order).select_related(
        "ticket", "ticket__passenger"
    )


def get_order_tickets_without_seat(order: Order) -> QuerySet[OrderTicket]:
    return OrderTicket.objects.filter(order=order, seat_number__isnull=True)


def get_selected_user_seat_ids(order: Order) -> QuerySet[OrderTicket]:
    return OrderTicket.objects.filter(
        order=order, seat_number__isnull=False
    ).values_list("seat_number", flat=True)


def get_selected_seat_ids(flight_pk: int) -> QuerySet[OrderTicket]:
    orders = Order.objects.filter(flight_id=flight_pk)
    return OrderTicket.objects.filter(
        order__in=orders, seat_id__isnull=False
    ).values_list("seat_id", flat=True)


def get_order_ticket_with_flight(order_ticket_pk: int) -> OrderTicket:
    return (
        OrderTicket.objects.select_related("order__flight")
        .filter(pk=order_ticket_pk)
        .first()
    )


def get_order_ticket_by_seat(seat_number: int) -> OrderTicket:
    return (
        OrderTicket.objects.select_related("order__flight")
        .filter(seat_number=seat_number)
        .first()
    )
