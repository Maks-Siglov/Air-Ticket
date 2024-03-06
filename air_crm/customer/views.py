from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from orders.models import Order


@login_required(login_url="users:login")
def profile(request: HttpRequest) -> HttpResponse:
    return render(request, "customer/profile.html")


@login_required(login_url="users:login")
def customer_orders(request: HttpRequest) -> HttpResponse:
    orders = Order.objects.filter(user=request.user)
    return render(request, "customer/orders.html", {"orders": orders})
