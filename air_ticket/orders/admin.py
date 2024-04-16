from django.contrib import admin

from orders.models import Order, OrderTicket


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "flight",
        "status",
        "total_price",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("id", "flight__number", "status")
    ordering = ("-id",)


@admin.register(OrderTicket)
class OrderTicketAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket", "order", "seat_number")
    list_filter = ("ticket", "order")
