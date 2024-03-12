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
from booking.models import TicketCart
from booking.selectors import (
    get_cart,
    get_cart_tickets,
    get_cart_total_price,
    get_ticket,
)
from customer.forms import PassengerForm
from customer.forms.contact import ContactForm
from customer.models import Contact

from flight.models import Flight
from flight.selectors import get_flight_with_seats


def create_cart(request: HttpRequest, flight_pk: int) -> HttpResponseRedirect:
    try:
        flight = Flight.objects.get(pk=flight_pk)
    except ObjectDoesNotExist:
        messages.error(request, "Flight does not exist")
        return redirect("main:index")

    passenger_amount = request.GET.get("passenger_amount")

    cart = TicketCart.objects.create(
        passenger_amount=passenger_amount, flight=flight
    )

    if request.user.is_authenticated:
        user = request.user
        try:
            contact = Contact.objects.get(email=user.email)
        except ObjectDoesNotExist:
            contact = Contact.objects.create(
                phone_number=user.phone_number,
                email=user.email,
            )
        cart.contact = contact
        cart.save()

    return redirect("booking:book", cart.pk)


def book(request: HttpRequest, cart_pk: int) -> HttpResponse:
    try:
        cart = get_cart(cart_pk)
    except ObjectDoesNotExist:
        messages.error(request, "Cart does not exist")
        return redirect("main:index")

    flight = get_flight_with_seats(cart.flight.pk)
    tickets = get_cart_tickets(cart)
    total_price = get_cart_total_price(cart)

    passenger_amount = cart.passenger_amount
    passengers = range(1, passenger_amount + 1)
    numbered_tickets = list(zip_longest(passengers, tickets))

    return render(
        request,
        "booking/booking.html",
        {
            "flight": flight,
            "passenger_amount": passenger_amount,
            "cart_pk": cart.pk,
            "tickets": tickets,
            "numbered_tickets": numbered_tickets,
            "contact": cart.contact,
            "total_price": total_price,
            "is_auth": request.user.is_authenticated,
        },
    )


def create_ticket(request: HttpRequest, cart_pk: int) -> JsonResponse:
    if request.method == "POST":
        try:
            cart = get_cart(cart_pk)
        except ObjectDoesNotExist:
            return JsonResponse({"error": "Flight does not exits"}, status=404)

        passenger_form = PassengerForm(request.POST)
        ticket_form = TicketForm(request.POST)
        if passenger_form.is_valid() and ticket_form.is_valid():
            with transaction.atomic():
                seat_type = ticket_form.cleaned_data["seat_type"]

                passenger = passenger_form.save()
                ticket = ticket_form.save(commit=False)
                ticket.passenger = passenger
                ticket.cart = cart
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
            ticket.save()
            passenger_form.save()

        return JsonResponse(
            {"message": "Ticket successfully updated"}, status=200
        )

    return JsonResponse({"Error": "Provided data not valid"}, status=400)


def create_contact(request, cart_pk: int) -> JsonResponse:
    try:
        cart = TicketCart.objects.get(pk=cart_pk)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "Cart does not exist"}, status=400)

    form = ContactForm(request.POST)
    if form.is_valid():
        contact = form.save()
        cart.contact = contact
        cart.save()

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
