from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from flight.admin.inlines import (
    BookingInline,
    CartInline,
    TicketInline
)
from flight.models import Flight


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    inlines = (TicketInline, BookingInline, CartInline)
    list_display = (
        "number",
        "iata",
        "icao",
        "airplane_link",
        "departure_airport_link",
        "arrival_airport_link",
        "departure_scheduled",
        "arrival_scheduled",
        "price",
        "lunch_price",
        "luggage_price",
    )
    list_filter = (
        "departure_scheduled",
        "arrival_scheduled",
        "airplane",
        "departure_airport",
        "arrival_airport",
    )
    search_fields = ("number", "iata", "icao")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related(
            "airplane", "arrival_airport", "departure_airport"
        )

    def airplane_link(self, obj):
        airplane = obj.airplane
        if airplane:
            url = reverse("admin:flight_airplane_change", args=(airplane.id,))
            return format_html('<a href="{}">{}</a>', url, airplane.name)
        else:
            return "-"

    def departure_airport_link(self, obj):
        airport = obj.departure_airport
        if airport:
            url = reverse("admin:flight_airport_change", args=(airport.id,))
            return format_html('<a href="{}">{}</a>', url, airport.name)
        else:
            return "-"

    def arrival_airport_link(self, obj):
        airport = obj.arrival_airport
        if airport:
            url = reverse("admin:flight_airport_change", args=(airport.id,))
            return format_html('<a href="{}">{}</a>', url, airport.name)
        else:
            return "-"

    airplane_link.short_description = "Airplane"
    departure_airport_link.short_description = "Departure Airport"
    arrival_airport_link.short_description = "Arrival Airport"
