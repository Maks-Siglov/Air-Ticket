from django.contrib import admin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.safestring import SafeString, mark_safe

from orders.models import OrderTicket


@admin.register(OrderTicket)
class OrderTicketAdmin(admin.ModelAdmin):
    list_display = ("id", "ticket_link", "order_link", "seat_number")
    list_filter = ("ticket", "order")

    def get_queryset(self, request) -> QuerySet[OrderTicket]:
        qs = super().get_queryset(request)
        return qs.select_related("order", "ticket")

    def ticket_link(self, obj: OrderTicket) -> SafeString | str:
        ticket = obj.ticket
        if ticket:
            url = reverse("admin:booking_ticket_change", args=(ticket.id,))
            link = f'<a href="{url}">{ticket}</a>'
            return mark_safe(link)
        else:
            return "-"

    def order_link(self, obj: OrderTicket) -> SafeString | str:
        order = obj.order
        if order:
            url = reverse("admin:orders_order_change", args=(order.id,))
            link = f'<a href="{url}">{order}</a>'
            return mark_safe(link)
        else:
            return "-"

    ticket_link.short_description = "Ticket"
    order_link.short_description = "Order"
