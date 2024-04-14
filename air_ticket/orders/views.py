from django.conf import settings
from django.contrib import messages
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
from django.shortcuts import redirect, render

from booking.crud import (
    get_cart_tickets,
    get_cart_total_price,
    order_update_booking,
    get_cart_with_contact,
)

from orders.crud import (
    get_order,
    get_order_with_flight,
    get_passenger_order_tickets,
)
from orders.models import Order, OrderTicket
from orders.services.tickets_email import tickets_email
from orders.services.user_creation_email import creation_user_email
from orders.stripe import stripe


def checkout(
    request: HttpRequest, cart_pk: int
) -> HttpResponse | HttpResponseRedirect:
    if (cart := get_cart_with_contact(cart_pk)) is None:
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
            "domain": settings.DOMAIN,
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
                            f" Passenger"
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
    order = get_order_with_flight(order_pk)
    order.status = "Completed"
    order.save()
    order_update_booking(order)

    if request.user.is_authenticated:
        tickets_email(request.user, order)
    else:
        creation_user_email(order)

    return redirect("orders:detail", order.pk)


def order_details(request: HttpRequest, order_pk: int) -> HttpResponse:
    order = get_order_with_flight(order_pk)
    order_tickets = get_passenger_order_tickets(order)
    return render(
        request,
        "orders/stripe/return.html",
        {
            "domain": settings.DOMAIN,
            "order": order,
            "order_tickets": order_tickets,
            "flight": order.flight,
            "total_price": order.total_price,
        },
    )
