from django.contrib import admin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.safestring import mark_safe

from booking.models import Booking


class BookingInline(admin.TabularInline):
    model = Booking
    extra = 0
    readonly_fields = ("cart_link", "ticket_link", "created_at")
    fields = (
        "ticket_link",
        "cart_link",
        "is_ordered",
        "is_active",
        "created_at",
    )

    def get_queryset(self, request) -> QuerySet[Booking]:
        queryset = super().get_queryset(request)
        return queryset.select_related("ticket", "cart", "flight")

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

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
            link = f'<a href="{url}">{ticket}</a>'
            return mark_safe(link)
        else:
            return "-"

    cart_link.short_description = "Cart"
    ticket_link.short_description = "Ticket"
