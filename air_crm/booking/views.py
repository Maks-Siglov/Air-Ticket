from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect

from customer.forms import PassengerForm

from flight.models import Flight

from booking.models import Ticket
from booking.selectors import get_seat


def book(request: HttpRequest, flight_pk: int) -> HttpResponse:
    try:
        flight = Flight.objects.get(pk=flight_pk)
    except ObjectDoesNotExist:
        messages.error(request, "Flight does not exist")
        return redirect("main:index")

    return render(
        request,
        "booking/booking.html",
        {"flight": flight}
    )


def create_ticket(request: HttpRequest, flight_pk: int) -> JsonResponse:
    if request.method == "POST":
        try:
            flight = Flight.objects.get(pk=flight_pk)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Flight does not exits"}, status=404)

        passenger_form = PassengerForm(request.POST)
        seat_type = request.POST.get("seat_type")

        if passenger_form.is_valid() and seat_type:
            passenger = passenger_form.save()

            seat = get_seat(flight.airplane, seat_type)

            ticket = Ticket.objects.create(
                passenger=passenger, seat=seat, price=10000
            )

            return JsonResponse(
                {
                    "ticket": {
                        "id": ticket.id,
                        "price": ticket.price,
                        "seat_type": seat.type
                    },
                    "passenger": {
                        "id": passenger.id,
                        "first_name": passenger.first_name,
                        "last_name": passenger.last_name
                    }
                }, status=201
            )

        return JsonResponse({"error": "Not valid form data"}, status=400)
