from django.contrib import admin
from django.db.models import QuerySet

from booking.models import (
    Booking,
    Ticket,
    TicketCart
)


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


@admin.register(TicketCart)
class TicketCartAdmin(admin.ModelAdmin):
    list_display = (
        "contact",
        "passenger_amount",
        "flight",
        "created_at",
        "updated_at",
    )
    list_filter = ("flight", "created_at")
    search_fields = ("contact__name", "flight__number")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "flight",
        "cart",
        "ticket",
        "is_ordered",
        "is_active",
        "created_at",
    )
    list_filter = ("is_ordered", "is_active", "created_at")
    search_fields = ("id", "flight__number", "cart__id", "ticket__id")
