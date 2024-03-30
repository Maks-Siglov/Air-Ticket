from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect, render

from booking.models import TicketCart
from booking.selectors import get_cart_tickets, get_cart_total_price
from booking.stripe import stripe

from flight.selectors import get_flight

from orders.services.tickets_email import send_tickets_email
from orders.services.user_creation_email import send_creation_user_email
from orders.models import Order
from orders.models.order_ticket import OrderTicket
from orders.selectors import get_order, get_passenger_order_tickets


def checkout(
    request: HttpRequest, cart_pk: int
) -> HttpResponse | HttpResponseRedirect:
    try:
        cart = TicketCart.objects.select_related("contact").get(pk=cart_pk)
    except ObjectDoesNotExist:
        messages.warning(request, "Cart does not exist")
        return redirect(request.META.get("HTTP_REFERER"))

    if cart.contact is None:
        messages.warning(request, "Please fill contact data")
        return redirect(request.META.get("HTTP_REFERER"))

    tickets = get_cart_tickets(cart)
    if tickets.count() != cart.passenger_amount:
        messages.warning(request, "Please fill all tickets for payment")
        return redirect(request.META.get("HTTP_REFERER"))

    total_price = get_cart_total_price(cart)
    order = Order.objects.create(flight=cart.flight, total_price=total_price)

    for ticket in tickets:
        OrderTicket.objects.create(order=order, ticket=ticket)

    return render(
        request,
        "orders/stripe/checkout.html",
        {
            "order_pk": order.pk,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY,
        },
    )


def create_checkout_session(request: HttpRequest, order_pk) -> JsonResponse:
    if request.method == "POST":
        order = get_order(order_pk)
        tickets = get_passenger_order_tickets(order)
        line_items = []
        for order_ticket in tickets:
            ticket = order_ticket.ticket
            data = {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": ticket.unit_amount,
                    "product_data": {
                        "name": (
                            f"{ticket.passenger.first_name} "
                            f"{ticket.passenger.last_name} "
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
                f"http://{settings.DOMAIN}/orders/{order.pk}"
                + "/return/?session_id={CHECKOUT_SESSION_ID}"
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
    order = get_order(order_pk)
    order.status = "Completed"
    order.save()

    if request.user.is_authenticated:
        send_tickets_email(request.user, order)
    else:
        send_creation_user_email(order)

    return redirect("orders:detail", order.pk)


def order_details(request: HttpRequest, order_pk: int) -> HttpResponse:
    order = get_order(order_pk)
    order_tickets = get_passenger_order_tickets(order)
    flight = get_flight(order.flight_id)
    return render(
        request,
        "orders/stripe/return.html",
        {
            "order": order,
            "order_tickets": order_tickets,
            "flight": flight,
            "total_price": order.total_price,
        },
    )
