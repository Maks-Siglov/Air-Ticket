from itertools import zip_longest

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect, render

from booking.forms import TicketForm
from booking.models import Order
from booking.selectors import (
    get_seat,
    get_flight,
    get_order_tickets,
    get_ticket,
    get_order,
    get_contact,
)
from customer.forms import PassengerForm
from customer.forms.contact import ContactForm
from customer.models.contact import Contact

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
        order = get_order(order_pk)
    except ObjectDoesNotExist:
        messages.error(request, "Order does not exist")
        return redirect("main:index")

    flight = get_flight(order.flight.pk)
    tickets = get_order_tickets(order)
    contact = get_contact(order)

    passenger_amount = order.passenger_amount
    passengers = range(1, passenger_amount + 1)
    numbered_tickets = list(zip_longest(passengers, tickets))

    return render(
        request,
        "booking/booking.html",
        {
            "flight": flight,
            "passenger_amount": passenger_amount,
            "order_pk": order.pk,
            "tickets": tickets,
            "numbered_tickets": numbered_tickets,
            "contact": contact,
        },
    )


def create_ticket(request: HttpRequest, flight_pk: int) -> JsonResponse:
    if request.method == "POST":
        try:
            flight = Flight.objects.get(pk=flight_pk)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Flight does not exits"}, status=404)

        passenger_form = PassengerForm(request.POST)
        ticket_form = TicketForm(request.POST)
        order_pk = request.POST.get("order_pk")
        if passenger_form.is_valid() and ticket_form.is_valid():
            try:
                order = Order.objects.get(pk=order_pk)
            except ObjectDoesNotExist:
                return JsonResponse(
                    {"error": "Order does not exist"}, status=400
                )
            passenger = passenger_form.save()

            seat_type = ticket_form.cleaned_data["seat_type"]
            seat = get_seat(flight.airplane, seat_type)

            ticket = ticket_form.save(commit=False)
            ticket.passenger = passenger
            ticket.order = order
            ticket.seat = seat
            ticket.save()

            return JsonResponse(
                {
                    "ticket_price": ticket.price,
                    "first_name": passenger.first_name,
                    "last_name": passenger.last_name,
                },
                status=201,
            )

        return JsonResponse({"error": "Not valid form data"}, status=400)


def update_ticket(request, ticket_pk: int) -> JsonResponse:
    try:
        ticket = get_ticket(ticket_pk)
    except ObjectDoesNotExist:
        return JsonResponse("Ticket does not exist", status=404)

    passenger = ticket.passenger
    ticket_form = TicketForm(request.POST, instance=ticket)
    passenger_form = PassengerForm(request.POST, instance=passenger)
    if ticket_form.is_valid() and passenger_form.is_valid():
        passenger_form.save()
        ticket = ticket_form.save(commit=False)
        seat_type = ticket_form.cleaned_data["seat_type"]
        seat = ticket.seat
        seat.type = seat_type
        seat.save()
        ticket.save()

        return JsonResponse(
            {
                "ticket_price": ticket.price,
                "first_name": passenger.first_name,
                "last_name": passenger.last_name,
            },
            status=200,
        )

    return JsonResponse({"Error": passenger_form.errors}, status=400)


def create_contact(request) -> JsonResponse:
    order_pk = request.POST.get("order_pk")
    try:
        order = Order.objects.get(pk=order_pk)
    except ObjectDoesNotExist:
        return JsonResponse(
            {"error": "Order does not exist"}, status=400
        )

    form = ContactForm(request.POST)
    if form.is_valid():
        contact = form.save(commit=False)
        contact.order = order
        contact.save()

        return JsonResponse({"success": "Contact created"}, status=201)

    return JsonResponse({"Error": form.errors}, status=400)


def update_contact(request, contact_pk: int) -> JsonResponse:
    try:
        contact = Contact.objects.get(pk=contact_pk)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Contact does not exist"}, status=404)

    form = ContactForm(request.POST, instance=contact)
    if form.is_valid():
        contact.save()

        return JsonResponse({"success": "Contact updated"}, status=200)

    return JsonResponse({"Error": form.errors}, status=400)
