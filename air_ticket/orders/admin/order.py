from django.contrib import admin
from django.db.models import QuerySet
from django.urls import reverse
from django.utils.safestring import SafeString, mark_safe

from booking.admin.inlines import OrderTicketInline
from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = (OrderTicketInline,)
    list_display = (
        "id",
        "user_link",
        "flight_link",
        "status",
        "total_price",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("id", "flight__number", "status")

    def get_queryset(self, request) -> QuerySet[Order]:
        qs = super().get_queryset(request)
        return qs.select_related("user", "flight")

    def user_link(self, obj: Order) -> SafeString | str:
        user = obj.user
        if user:
            url = reverse("admin:users_user_change", args=(user.id,))
            link = f'<a href="{url}">{user}</a>'
            return mark_safe(link)
        else:
            return "-"

    def flight_link(self, obj: Order) -> SafeString | str:
        flight = obj.flight
        if flight:
            url = reverse("admin:flight_flight_change", args=(flight.id,))
            link = f'<a href="{url}">{flight}</a>'
            return mark_safe(link)
        else:
            return "-"

    user_link.short_description = "User"
    flight_link.short_description = "Flight"
