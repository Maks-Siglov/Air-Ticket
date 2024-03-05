from itertools import zip_longest

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
from booking.selectors import get_seat, get_flight, get_order_tickets

from customer.forms import PassengerForm
from customer.models import Passenger

from flight.models import Flight


def create_order(request: HttpRequest, flight_pk: int) -> HttpResponseRedirect:
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

    passengers = range(1, passenger_amount + 1)
    numbered_tickets = list(zip_longest(passengers, tickets))

    print(numbered_tickets)

    return render(
        request,
        "booking/booking.html",
        {
            "flight": flight,
            "passenger_amount": passenger_amount,
            "order_pk": order.pk,
            "tickets": tickets,
            "numbered_tickets": numbered_tickets
        },
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
                order=order,
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


def update_ticket(request, ticket_pk: int) -> JsonResponse:
    try:
        ticket = Ticket.objects.select_related("passenger").get(pk=ticket_pk)
    except ObjectDoesNotExist:
        return JsonResponse("Ticket does not exist", status=404)

    passenger = ticket.passenger
    passenger_form = PassengerForm(request.POST, instance=passenger)
    if passenger_form.is_valid():
        passenger_form.save()

        seat_type = request.POST.get("seat_type")
        price = request.POST.get("price")

        ticket.seat_type = seat_type
        ticket.price = price

        ticket.save()
        return JsonResponse({"message": "Ticket updated"}, status=200)

    return JsonResponse({"Error": passenger_form.errors}, status=400)





def checkout(
    request: HttpRequest, order_pk: int
) -> HttpResponse | HttpResponseRedirect:
    try:
        order = Order.objects.get(pk=order_pk)
    except ObjectDoesNotExist:
        messages.error(request, "Ticket does not exist")
        return redirect(request.META.get("HTTP_REFERER"))

    order.status = "Processed"
    order.save()

    return render(
        request, "booking/stripe/checkout.html", {"order_pk": order_pk}
    )


def create_checkout_session(request: HttpRequest, order_pk) -> JsonResponse:
    if request.method == "POST":
        order = Order.objects.get(pk=order_pk)
        tickets = get_order_tickets(order)
        line_items = []
        for ticket in tickets:
            data = {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": ticket.price,
                    "product_data": {
                        "name": (
                            f"{ticket.passenger.first_name} "
                            f"{ticket.passenger.last_name} "
                            f"Ticket №{ticket.pk}"
                        )
                    },
                },
                "quantity": 1,
            }
            line_items.append(data)
        checkout_session = stripe.checkout.Session.create(
            ui_mode="embedded",
            line_items=line_items,
            mode="payment",
            return_url=(
                f"http://{settings.DOMAIN}/booking/{order.pk}"
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


def checkout_return(
    request: HttpRequest, order_pk: int
) -> HttpResponseRedirect:
    order = Order.objects.get(pk=order_pk)
    order.status = "Completed"
    order.save()
    return redirect("booking:detail", order.pk)


def order_details(request: HttpRequest, order_pk: int) -> HttpResponse:
    order = Order.objects.get(pk=order_pk)
    return render(request, "booking/stripe/return.html", {"order": order})
