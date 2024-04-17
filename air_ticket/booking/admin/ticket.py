from django.contrib import admin
from django.db.models import QuerySet

from booking.models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "price",
        "flight",
        "passenger",
        "cart",
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
