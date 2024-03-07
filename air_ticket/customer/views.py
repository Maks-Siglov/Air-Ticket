from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from flight.selectors import get_user_flights
from orders.models import Order


@login_required(login_url="users:login")
def profile(request: HttpRequest) -> HttpResponse:
    return render(request, "customer/profile.html")


@login_required(login_url="users:login")
def customer_orders(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.filter(user=request.user)
    return render(request, "customer/orders.html", {"orders": orders})


@login_required(login_url="users:login")
def customer_flights(request: HttpRequest) -> HttpResponse:
    selected_status = request.GET.get("status")

    flights = get_user_flights(request.user, selected_status)

    return render(request, "customer/flights.html", {"flights": flights})
