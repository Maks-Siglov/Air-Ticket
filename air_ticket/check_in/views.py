from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from flight.selectors import get_flight
from orders.selectors import (
    get_order,
    get_order_tickets_without_seat,
    get_selected_seat_ids,
    get_selected_user_seat_ids,
)


@login_required(login_url="users:login")
def check_in(request: HttpRequest, order_pk: int) -> HttpResponse:
    try:
        order = get_order(order_pk)
    except ObjectDoesNotExist:
        messages.warning(request, "Order for check-in not exit")
        return redirect("customer:profile")

    flight_pk = order.flight_id
    flight = get_flight(flight_pk)
    tickets = get_order_tickets_without_seat(order)
    ticket_ids = list(tickets.values_list("id", flat=True))
    user_seat_ids = list(get_selected_user_seat_ids(order))
    selected_seat_ids = list(get_selected_seat_ids(flight_pk))
    return render(
        request,
        "check_in/check_in.html",
        {
            "flight": flight,
            "flight_pk": flight_pk,
            "tickets_amount": tickets.count(),
            "ticket_ids": ticket_ids,
            "user_seat_ids": user_seat_ids,
            "selected_seat_ids": selected_seat_ids,
        },
    )
