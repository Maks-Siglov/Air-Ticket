from django.db.models import QuerySet

from orders.models import Order
from orders.models.order_ticket import OrderTicket

from users.models import User


def get_order(order_pk: int) -> Order:
    return Order.objects.get(pk=order_pk)


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
    return OrderTicket.objects.filter(order=order, seat__isnull=True)


def get_selected_user_seat_ids(order: Order) -> QuerySet[OrderTicket]:
    return OrderTicket.objects.filter(
        order=order, seat__isnull=False
    ).values_list("seat_id", flat=True)


def get_selected_seat_ids(flight_pk: int) -> QuerySet[OrderTicket]:
    order_ids = Order.objects.filter(flight_id=flight_pk).values_list(
        "id", flat=True
    )
    return OrderTicket.objects.filter(
        order_id__in=order_ids, seat_id__isnull=False
    ).values_list("seat_id", flat=True)
