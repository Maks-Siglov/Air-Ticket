from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from orders.crud import (
    get_order_tickets_without_seat,
    get_order_with_flight,
    get_selected_seat_ids,
    get_selected_user_seat_ids
)


@login_required(login_url="users:login")
def check_in(request: HttpRequest, order_pk: int) -> HttpResponse:
    if (order := get_order_with_flight(order_pk)) is None:
        messages.warning(request, "Order for check-in not exit")
        return redirect("customer:profile")

    flight_pk = order.flight_id
    tickets = get_order_tickets_without_seat(order)
    ticket_ids = list(tickets.values_list("id", flat=True))
    user_seat_ids = list(get_selected_user_seat_ids(order))
    selected_seat_ids = list(get_selected_seat_ids(flight_pk))
    return render(
        request,
        "check_in/check_in.html",
        {
            "flight": order.flight,
            "flight_pk": flight_pk,
            "tickets_amount": tickets.count(),
            "ticket_ids": ticket_ids,
            "user_seat_ids": user_seat_ids,
            "selected_seat_ids": selected_seat_ids,
        },
    )
