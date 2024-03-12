from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from flight.selectors import get_flight
from orders.selectors import get_order, get_order_tickets


@login_required(login_url="users:login")
def check_in(request: HttpRequest, order_pk: int) -> HttpResponse:
    try:
        order = get_order(order_pk)
    except ObjectDoesNotExist:
        messages.warning(request, "Order for check-in not exit")
        return redirect("customer:profile")

    flight_pk = order.flight_id
    flight = get_flight(flight_pk)
    tickets = get_order_tickets(order)

    return render(
        request,
        "check_in/check_in.html",
        {
            "flight": flight,
            "flight_pk": flight_pk,
            "tickets_amount": tickets.count(),
        },
    )
