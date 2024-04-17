from django.contrib import admin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.safestring import mark_safe

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
        "cart_link",
        "price",
        "lunch",
        "luggage",
    )

    def get_queryset(self, request) -> QuerySet[Ticket]:
        queryset = super().get_queryset(request)
        return queryset.select_related("passenger", "cart", "flight")

    def passenger_first_name_link(self, obj):
        passenger = obj.passenger
        if passenger:
            url = reverse(
                "admin:customer_passenger_change", args=(passenger.id,)
            )
            link = f'<a href="{url}">{passenger.first_name}</a>'
            return mark_safe(link)
        else:
            return "-"

    def passenger_last_name_link(self, obj):
        passenger = obj.passenger
        if passenger:
            url = reverse(
                "admin:customer_passenger_change", args=(passenger.id,)
            )
            link = f'<a href="{url}">{passenger.last_name}</a>'
            return mark_safe(link)
        else:
            return "-"

    def cart_link(self, obj):
        cart = obj.cart
        if cart:
            url = reverse("admin:booking_ticketcart_change", args=(cart.id,))
            link = f'<a href="{url}">{cart}</a>'
            return mark_safe(link)
        else:
            return "-"

    passenger_first_name_link.short_description = "First Name"
    passenger_last_name_link.short_description = "Last Name"
    cart_link.short_description = "Cart"
