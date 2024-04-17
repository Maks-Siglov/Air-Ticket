from django.contrib import admin
from django.db.models import QuerySet

from orders.models import OrderTicket


class OrderTicketInline(admin.StackedInline):
    model = OrderTicket
    extra = 0

    def get_queryset(self, request) -> QuerySet[OrderTicket]:
        qs = super().get_queryset(request)
        return qs.select_related("order")

    def has_delete_permission(self, request, obj=None) -> bool:
        return False
