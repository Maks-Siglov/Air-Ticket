from itertools import zip_longest

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from booking.models import Booking, TicketCart
from booking.selectors import (
    get_cart_tickets,
    get_cart_total_price,
    get_cart_with_flight,
)
from customer.models import Contact
from flight.models import Flight
from flight.selectors import get_flight_with_seats


def create_cart(request: HttpRequest, flight_pk: int) -> HttpResponseRedirect:
    try:
        flight = Flight.objects.get(pk=flight_pk)
    except ObjectDoesNotExist:
        messages.error(request, "Flight does not exist")
        return redirect("main:index")

    passenger_amount = int(request.GET.get("passenger_amount"))

    cart = TicketCart.objects.create(
        passenger_amount=passenger_amount, flight=flight
    )

    bookings = [
        Booking(flight=flight, cart=cart) for _ in range(passenger_amount)
    ]
    Booking.objects.bulk_create(bookings)

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
        cart = get_cart_with_flight(cart_pk)
    except ObjectDoesNotExist:
        messages.error(request, "Cart does not exist")
        return redirect("main:index")

    flight = get_flight_with_seats(cart.flight_id)
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
