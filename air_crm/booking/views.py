from django.contrib import messages
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect, render

from booking.stripe import stripe
from booking.models import Ticket, Order
from booking.selectors import get_seat, get_flight

from customer.forms import PassengerForm

from flight.models import Flight


def create_order(
        request: HttpRequest, flight_pk: int
) -> HttpResponseRedirect:
    try:
        flight = Flight.objects.get(pk=flight_pk)
    except ObjectDoesNotExist:
        messages.error(request, "Flight does not exist")
        return redirect("main:index")

    passenger_amount = request.GET.get("passenger_amount")

    order = Order.objects.create(
        passenger_amount=passenger_amount, flight=flight
    )

    return redirect("booking:book", order.pk)


def book(request: HttpRequest, order_pk: int) -> HttpResponse:
    try:
        order = Order.objects.select_related("flight").get(pk=order_pk)
    except ObjectDoesNotExist:
        messages.error(request, "Order does not exist")
        return redirect("main:index")

    tickets = Ticket.objects.filter(order=order)
    flight = get_flight(order.flight.pk)
    passenger_amount = order.passenger_amount

    return render(
        request,
        "booking/booking.html",
        {
            "flight": flight,
            "passenger_amount": passenger_amount,
            "passengers": range(passenger_amount),
            "order_pk": order.pk,
            "tickets": tickets
        }
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
        order_pk = request.POST.get("order_pk")
        if passenger_form.is_valid() and seat_type:
            try:
                order = Order.objects.get(pk=order_pk)
            except ObjectDoesNotExist:
                return JsonResponse(
                    {"error": "Order does not exist"}, status=400
                )

            passenger = passenger_form.save()
            seat = get_seat(flight.airplane, seat_type)

            ticket = Ticket.objects.create(
                passenger=passenger,
                seat=seat,
                price=int(price) * 100,
                order=order
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
                        "passport_id": passenger.passport_id,
                        "first_name": passenger.first_name,
                        "last_name": passenger.last_name,
                    },
                },
                status=201,
            )

        return JsonResponse({"error": "Not valid form data"}, status=400)


def checkout(
        request: HttpRequest, ticket_pk: int
) -> HttpResponse | HttpResponseRedirect:
    try:
        Ticket.objects.get(pk=ticket_pk)
    except ObjectDoesNotExist:
        messages.error(request, "Ticket does not exist")
        return redirect(request.META.get("HTTP_REFERER"))

    return render(
        request, "booking/stripe/checkout.html", {"ticket_pk": ticket_pk}
    )


def create_checkout_session(
        request: HttpRequest, ticket_pk
) -> JsonResponse:
    if request.method == "POST":
        ticket = Ticket.objects.get(pk=ticket_pk)

        data = (
            {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": ticket.price,
                    "product_data": {
                        "name": f"Ticket №{ticket_pk}",
                    },
                },
                "quantity": 1,
            },
        )
        checkout_session = stripe.checkout.Session.create(
            ui_mode="embedded",
            line_items=data,
            mode="payment",
            return_url=(
                    f"http://{settings.DOMAIN}/booking/{ticket_pk}"
                    + "/return?session_id={CHECKOUT_SESSION_ID}"
            ),
        )
        return JsonResponse({"clientSecret": checkout_session.client_secret})


def session_status(request: HttpRequest):
    session = stripe.checkout.Session.retrieve(request.GET.get("session_id"))
    return JsonResponse(
        {
            "status": session.status,
            "customer_email": session.customer_details.email,
        }
    )


def checkout_return(request: HttpRequest, ticket_pk: int) -> HttpResponse:
    ticket = Ticket.objects.get(id=ticket_pk)
    return render(
        request,
        "booking/stripe/return.html",
        {"ticket": ticket}
    )
