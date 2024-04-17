from django.contrib import admin

from booking.models import TicketCart


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
