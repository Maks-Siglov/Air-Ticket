from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from booking.models import TicketCart


class CartInline(admin.TabularInline):
    model = TicketCart
    extra = 0
    readonly_fields = ("created_at", "updated_at")
    fields = (
        "contact",
        "passenger_amount",
        "flight",
        "created_at",
        "updated_at",
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related("contact", "flight")
