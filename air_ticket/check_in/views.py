from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from flight.selectors import get_flight, get_airplane_seats


@login_required(login_url="users:login")
def check_in(request: HttpRequest, flight_pk: int) -> HttpResponse:
    try:
        flight = get_flight(flight_pk)
    except ObjectDoesNotExist:
        messages.warning(request, "Flight for check-in not exit")
        return redirect("customer:profile")

    seats = get_airplane_seats(flight.airplane)
    seats_count = seats.count()

    return render(
        request,
        "check_in/check_in.html",
        {
            "flight": flight,
            "flight_pk": flight_pk,
        }
    )
