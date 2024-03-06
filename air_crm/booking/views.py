from itertools import zip_longest

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect, render

from booking.forms import TicketForm
from booking.selectors import get_contact, get_ticket

from customer.forms import PassengerForm
from customer.forms.contact import ContactForm
from customer.models.contact import Contact

from flight.models import Flight
from flight.selectors import get_flight, get_seat

from orders.models import Order
from orders.selectors import (
    get_order,
    get_order_tickets,
    get_order_total_price,
)


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
    total_price = get_order_total_price(order)

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
            "total_price": total_price,
        },
    )


def create_ticket(request: HttpRequest, flight_pk: int) -> JsonResponse:
    if request.method == "POST":
        try:
            flight = Flight.objects.get(pk=flight_pk)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Flight does not exits"}, status=404)

        order_pk = request.POST.get("order_pk")
        order = Order.objects.get(pk=order_pk)

        passenger_form = PassengerForm(request.POST)
        ticket_form = TicketForm(request.POST)
        if passenger_form.is_valid() and ticket_form.is_valid():
            with transaction.atomic():
                seat_type = ticket_form.cleaned_data["seat_type"]
                seat = get_seat(flight.airplane, seat_type)
                if seat is None:
                    return JsonResponse(
                        {"error": f"{seat_type} seat not available"},
                        status=400,
                    )
                seat.is_available = False
                seat.save()
                passenger = passenger_form.save()
                ticket = ticket_form.save(commit=False)
                ticket.passenger = passenger
                ticket.order = order
                ticket.seat = seat
                ticket.save()

                return JsonResponse(
                    {"message": "Ticket successfully created"}, status=201
                )

        return JsonResponse({"error": "Provided data not valid"}, status=400)


def update_ticket(request, ticket_pk: int) -> JsonResponse:
    try:
        ticket = get_ticket(ticket_pk)
    except ObjectDoesNotExist:
        return JsonResponse("Ticket does not exist", status=404)

    passenger = ticket.passenger
    ticket_form = TicketForm(request.POST, instance=ticket)
    passenger_form = PassengerForm(request.POST, instance=passenger)
    if passenger_form.is_valid() and ticket_form.is_valid():
        with transaction.atomic():
            seat_type = ticket_form.cleaned_data["seat_type"]
            ticket = ticket_form.save(commit=False)

            if ticket.seat.type != seat_type:
                seat = ticket.seat
                seat.is_available = True
                seat.save()
                new_seat = get_seat(seat.airplane, seat_type)
                if new_seat is None:
                    return JsonResponse(
                        {"error": f"{seat_type} seat not available"},
                        status=400,
                    )
                new_seat.is_available = False
                new_seat.save()
                ticket.seat = new_seat

            ticket.save()
            passenger_form.save()

        return JsonResponse(
            {"message": "Ticket successfully updated"}, status=200
        )

    return JsonResponse({"Error": "Provided data not valid"}, status=400)


def create_contact(request) -> JsonResponse:
    order_pk = request.POST.get("order_pk")
    try:
        order = Order.objects.get(pk=order_pk)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Order does not exist"}, status=400)

    form = ContactForm(request.POST)
    if form.is_valid():
        contact = form.save(commit=False)
        contact.order = order
        contact.save()

        return JsonResponse({"success": "Contact created"}, status=201)

    return JsonResponse({"error": "Provided data not valid"}, status=400)


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
