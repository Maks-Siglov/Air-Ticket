from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

from flight.selectors import get_user_flights, get_flight, get_airplane_seats
from orders.selectors import get_user_orders


@login_required(login_url="users:login")
def profile(request: HttpRequest) -> HttpResponse:
    return render(request, "customer/profile.html")


@login_required(login_url="users:login")
def customer_orders(request: HttpRequest) -> HttpResponse:
    page = request.GET.get("page", settings.DEFAULT_PAGE)

    orders = get_user_orders(request.user)

    paginator = Paginator(orders, settings.ITEMS_PER_PAGE)
    current_page = paginator.page(int(page))
    return render(request, "customer/orders.html", {"orders": current_page})


@login_required(login_url="users:login")
def customer_flights(request: HttpRequest) -> HttpResponse:
    selected_status = request.GET.get("status")
    page = request.GET.get("page", settings.DEFAULT_PAGE)

    flights = get_user_flights(request.user, selected_status)

    paginator = Paginator(flights, settings.ITEMS_PER_PAGE)
    current_page = paginator.page(int(page))
    return render(request, "customer/flights.html", {"flights": current_page})


@login_required(login_url="users:login")
def check_in(request: HttpRequest, flight_pk: int) -> HttpResponse:
    try:
        flight = get_flight(flight_pk)
    except ObjectDoesNotExist:
        messages.warning(request, "Flight for check-in not exit")
        return redirect("customer:profile")

    seats = get_airplane_seats(flight.airplane)
    seats_count = seats.count()

    return render(
        request,
        "customer/check_in.html",
        {
            "flight": flight,
            "seats": seats,
            "seats_count": seats_count,
        }
    )
