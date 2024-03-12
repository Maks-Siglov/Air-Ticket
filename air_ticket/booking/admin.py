from django.contrib import admin

from booking.models import Ticket


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("id", "passenger", "price", "cart")
    search_fields = ("id", "passenger__first_name", "passenger__last_name")
    ordering = ("-id",)
    readonly_fields = ("unit_amount",)
