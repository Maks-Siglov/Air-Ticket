from django.contrib import admin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.safestring import mark_safe

from booking.models import TicketCart
from flight.admin.inlines import TicketInline, BookingInline


@admin.register(TicketCart)
class TicketCartAdmin(admin.ModelAdmin):
    inlines = (TicketInline, BookingInline)
    list_display = (
        "id",
        "flight_link",
        "passenger_amount",
        "contact_link",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at",)
    search_fields = ("contact__name", "flight__number")

    def get_queryset(self, request) -> QuerySet[TicketCart]:
        qs = super().get_queryset(request)
        return qs.select_related("contact", "flight")

    def contact_link(self, obj):
        contact = obj.contact
        if contact:
            url = reverse("admin:customer_contact_change", args=(contact.id,))
            link = f'<a href="{url}">{contact}</a>'
            return mark_safe(link)
        else:
            return "-"

    def flight_link(self, obj):
        flight = obj.flight
        if flight:
            url = reverse("admin:flight_flight_change", args=(flight.id,))
            link = f'<a href="{url}">{flight}</a>'
            return mark_safe(link)
        else:
            return "-"
