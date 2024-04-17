from django.contrib import admin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.safestring import mark_safe

from booking.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "flight_link",
        "cart_link",
        "ticket_link",
        "is_ordered",
        "is_active",
        "created_at",
    )
    list_filter = ("is_ordered", "is_active", "created_at")
    search_fields = ("id", "flight_link", "cart_link")

    def get_queryset(self, request) -> QuerySet[Booking]:
        qs = super().get_queryset(request)
        return qs.select_related("cart", "flight", "ticket")

    def flight_link(self, obj):
        flight = obj.flight
        if flight:
            url = reverse("admin:flight_flight_change", args=(flight.id,))
            link = f'<a href="{url}">{flight}</a>'
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

    def ticket_link(self, obj):
        ticket = obj.ticket
        if ticket:
            url = reverse("admin:booking_ticket_change", args=(ticket.id,))
            link = f"<a href='{url}'>{ticket}</a>"
            return mark_safe(link)
        else:
            return "-"

    ticket_link.short_description = "Ticket"
    flight_link.short_description = "Flight"
    cart_link.short_description = "Cart"
