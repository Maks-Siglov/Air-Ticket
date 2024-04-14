from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from flight.crud import get_user_flights
from orders.crud import get_user_orders


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
def customer_check_ins(request: HttpRequest) -> HttpResponse:
    orders = get_user_orders(request.user)
    return render(request, "customer/check_in.html", {"orders": orders})
