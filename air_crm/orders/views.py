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

from booking.models import Ticket
from booking.stripe import stripe
from customer.models.contact import Contact
from flight.selectors import get_flight
from orders.models import Order
from orders.selectors import (
    get_order_tickets,
    get_order_total_price,
    get_order,
)


def checkout(
    request: HttpRequest, order_pk: int
) -> HttpResponse | HttpResponseRedirect:
    try:
        order = Order.objects.get(pk=order_pk)
    except ObjectDoesNotExist:
        messages.warning(request, "Order does not exist")
        return redirect(request.META.get("HTTP_REFERER"))
    try:
        Contact.objects.get(order=order)
    except ObjectDoesNotExist:
        messages.warning(request, "Please fill contact data")
        return redirect(request.META.get("HTTP_REFERER"))

    tickets_count = Ticket.objects.filter(order=order).count()
    if tickets_count != order.passenger_amount:
        messages.warning(request, "Please fill all tickets for payment")
        return redirect(request.META.get("HTTP_REFERER"))

    order.status = "Processed"
    order.save()

    return render(
        request, "orders/stripe/checkout.html", {"order_pk": order_pk}
    )


def create_checkout_session(request: HttpRequest, order_pk) -> JsonResponse:
    if request.method == "POST":
        order = Order.objects.get(pk=order_pk)
        tickets = get_order_tickets(order)
        line_items = []
        for ticket in tickets:
            data = {
                "price_data": {
                    "currency": "usd",
                    "unit_amount": ticket.unit_amount,
                    "product_data": {
                        "name": (
                            f"{ticket.passenger.first_name} "
                            f"{ticket.passenger.last_name} "
                            f"{ticket.seat.type} Ticket "
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
                + "/return?session_id={CHECKOUT_SESSION_ID}"
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
    order = Order.objects.get(pk=order_pk)
    order.status = "Completed"
    order.save()
    return redirect("orders:detail", order.pk)


def order_details(request: HttpRequest, order_pk: int) -> HttpResponse:
    order = get_order(order_pk)
    total_price = get_order_total_price(order)

    tickets = get_order_tickets(order)
    flight = get_flight(order.flight.pk)
    return render(
        request,
        "orders/stripe/return.html",
        {
            "order": order,
            "tickets": tickets,
            "flight": flight,
            "total_price": total_price,
        },
    )
