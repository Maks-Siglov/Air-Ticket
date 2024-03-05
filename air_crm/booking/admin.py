from django.contrib import admin
from booking.models import Order, Ticket


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "passenger_amount", "flight", "status")
    list_filter = ("status",)
    search_fields = ("id", "flight__number", "status")
    ordering = ("-id",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "passenger", "seat", "price", "order")
    list_filter = ("seat__type",)
    search_fields = ("id", "passenger__first_name", "passenger__last_name")
    ordering = ("-id",)
    readonly_fields = ("unit_amount",)
