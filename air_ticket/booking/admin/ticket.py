from django.contrib import admin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.safestring import SafeString, mark_safe

from booking.admin.inlines import OrderTicketInline
from booking.models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    inlines = (OrderTicketInline,)
    list_display = (
        "id",
        "flight_link",
        "passenger_link",
        "cart_link",
        "price",
        "created_at",
        "updated_at",
        "lunch",
        "luggage",
    )
    list_filter = ("lunch", "luggage", "flight", "created_at")
    search_fields = ("flight__number", "passenger__name")

    def get_queryset(self, request) -> QuerySet[Ticket]:
        qs = super().get_queryset(request)
        return qs.select_related("flight", "passenger", "cart")

    def flight_link(self, obj: Ticket) -> SafeString | str:
        flight = obj.flight
        if flight:
            url = reverse("admin:flight_flight_change", args=(flight.id,))
            link = f'<a href="{url}">{flight}</a>'
            return mark_safe(link)
        else:
            return "-"

    def passenger_link(self, obj: Ticket) -> SafeString | str:
        passenger = obj.passenger
        if passenger:
            url = reverse(
                "admin:customer_passenger_change", args=(passenger.id,)
            )
            link = f'<a href="{url}">{passenger}</a>'
            return mark_safe(link)
        else:
            return "-"

    def cart_link(self, obj: Ticket) -> SafeString | str:
        cart = obj.cart
        if cart:
            url = reverse("admin:booking_ticketcart_change", args=(cart.id,))
            link = f'<a href="{url}">{cart}</a>'
            return mark_safe(link)
        else:
            return "-"

    flight_link.short_description = "Flight"
    passenger_link.short_description = "Passenger"
    cart_link.short_description = "Cart"
