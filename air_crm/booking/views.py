from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render

from booking.models import Ticket
from booking.selectors import get_seat, get_flight

from customer.forms import PassengerForm

from flight.models import Flight


def book(request: HttpRequest, flight_pk: int) -> HttpResponse:
    try:
        flight = get_flight(flight_pk)
    except ObjectDoesNotExist:
        messages.error(request, "Flight does not exist")
        return redirect("main:index")
    passenger_amount = request.GET.get("passenger_amount")

    return render(
        request,
        "booking/booking.html",
        {"flight": flight, "passenger_amount": passenger_amount}
    )


def create_ticket(request: HttpRequest, flight_pk: int) -> JsonResponse:
    if request.method == "POST":
        try:
            flight = Flight.objects.get(pk=flight_pk)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Flight does not exits"}, status=404)

        passenger_form = PassengerForm(request.POST)
        seat_type = request.POST.get("seat_type")
        price = request.POST.get("price")
        print(int(price) * 100)

        if passenger_form.is_valid() and seat_type:
            passenger = passenger_form.save()

            seat = get_seat(flight.airplane, seat_type)

            ticket = Ticket.objects.create(
                passenger=passenger, seat=seat, price=int(price) * 100
            )

            return JsonResponse(
                {
                    "ticket": {
                        "id": ticket.id,
                        "price": ticket.price,
                        "seat_type": seat.type,
                    },
                    "passenger": {
                        "id": passenger.id,
                        "first_name": passenger.first_name,
                        "last_name": passenger.last_name,
                    },
                },
                status=201,
            )

        return JsonResponse({"error": "Not valid form data"}, status=400)
