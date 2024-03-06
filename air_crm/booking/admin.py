from django.contrib import admin

from booking.models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "passenger", "seat", "price", "cart")
    list_filter = ("seat__type",)
    search_fields = ("id", "passenger__first_name", "passenger__last_name")
    ordering = ("-id",)
    readonly_fields = ("unit_amount",)
