from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from flight.models import Flight


def book(request: HttpRequest, flight_pk: int) -> HttpResponse:
    try:
        flight = Flight.objects.get(pk=flight_pk)
    except ObjectDoesNotExist:
        messages.error(request, "Flight does not exist")
        return redirect("main:index")

    return render(
        request,
        "orders/booking.html",
        {"flight": flight}
    )
