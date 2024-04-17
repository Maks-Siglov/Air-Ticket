from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from booking.models import Ticket


class TicketInline(admin.TabularInline):
    model = Ticket
    extra = 1

    readonly_fields = (
        "passenger_first_name_link",
        "passenger_last_name_link",
        "cart_link",
    )
    fields = (
        "passenger_first_name_link",
        "passenger_last_name_link",
        "passenger",
        "cart_link",
        "price",
        "lunch",
        "luggage",
    )

    def passenger_first_name_link(self, obj):
        passenger = obj.passenger
        if passenger:
            url = reverse(
                "admin:customer_passenger_change", args=(passenger.id,)
            )
            return format_html(
                '<a href="{}">{}</a>', url, passenger.first_name
            )
        else:
            return "-"

    def passenger_last_name_link(self, obj):
        passenger = obj.passenger
        if passenger:
            url = reverse(
                "admin:customer_passenger_change", args=(passenger.id,)
            )
            return format_html('<a href="{}">{}</a>', url, passenger.last_name)
        else:
            return "-"

    def cart_link(self, obj):
        cart = obj.cart
        if cart:
            url = reverse("admin:booking_ticketcart_change", args=(cart.id,))
            return format_html('<a href="{}">{}</a>', url, cart)
        else:
            return "-"

    passenger_first_name_link.short_description = "First Name"
    passenger_last_name_link.short_description = "Last Name"
    cart_link.short_description = "Cart"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related(
            "passenger",
            "cart",
            "flight",
        )
