from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from booking.models import TicketCart


class CartInline(admin.TabularInline):
    model = TicketCart
    extra = 0
    readonly_fields = ("contact_link", "created_at", "updated_at")
    fields = (
        "contact_link",
        "passenger_amount",
        "flight",
        "created_at",
        "updated_at",
    )

    def contact_link(self, obj):
        contact = obj.contact
        if contact:
            url = reverse("admin:customer_contact_change", args=(contact.id,))
            return format_html('<a href="{}">{}</a>', url, contact)
        else:
            return "-"

    contact_link.short_description = "Contact"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("contact")
