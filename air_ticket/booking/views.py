import typing as t
from decimal import Decimal
from itertools import zip_longest

from django.contrib import messages
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect
)
from django.shortcuts import redirect, render

from booking.crud import (
    get_cart_tickets,
    get_cart_total_price,
    get_cart_with_flight_data
)
from booking.models import Booking, TicketCart
from customer.crud import get_contact_by_email
from customer.models import Contact
from flight.crud import book_available_seats
from flight.models import Flight
from users.models import User


def create_cart(request: HttpRequest, flight_pk: int) -> HttpResponseRedirect:
    if (flight := Flight.objects.filter(pk=flight_pk).first()) is None:
        messages.error(request, "Flight does not exist")
        return redirect("main:index")

    passenger_amount = request.GET.get("passenger_amount")
    if passenger_amount is None or not passenger_amount.isdigit():
        messages.error(request, "Passenger amount not provided")
        return redirect("main:index")
    passenger_amount = int(passenger_amount)

    cart = TicketCart.objects.create(
        passenger_amount=passenger_amount, flight=flight
    )
    try:
        chosen_seats = book_available_seats(flight, passenger_amount)
    except ValueError:
        messages.error(request, "There is no enough available seats")
        return redirect("main:index")
    bookings = [
        Booking(flight=flight, cart=cart, booked_seat_number=seat_number)
        for seat_number in chosen_seats
    ]
    Booking.objects.bulk_create(bookings)

    if request.user.is_authenticated:
        user = t.cast(User, request.user)

        if (contact := get_contact_by_email(user.email)) is None:
            contact = Contact.objects.create(
                phone_number=user.phone_number,
                email=user.email,
            )
        cart.contact = contact
        cart.save()

    return redirect("booking:book", cart.pk)


def book(request: HttpRequest, cart_pk: int) -> HttpResponse:
    if (cart := get_cart_with_flight_data(cart_pk)) is None:
        messages.error(request, "Cart does not exist")
        return redirect("main:index")
    flight = cart.flight

    tickets = get_cart_tickets(cart)
    total_price = get_cart_total_price(cart)

    if total_price is None:
        total_price = Decimal(0)

    passenger_amount = cart.passenger_amount
    passengers = range(1, passenger_amount + 1)
    numbered_tickets = list(zip_longest(passengers, tickets))

    return render(
        request,
        "booking/booking.html",
        {
            "flight": flight,
            "price": flight.price,
            "luggage_price": flight.luggage_price,
            "lunch_price": flight.lunch_price,
            "passenger_amount": passenger_amount,
            "cart_pk": cart.pk,
            "tickets": tickets,
            "numbered_tickets": numbered_tickets,
            "contact": cart.contact,
            "total_price": total_price,
            "is_auth": request.user.is_authenticated,
        },
    )
