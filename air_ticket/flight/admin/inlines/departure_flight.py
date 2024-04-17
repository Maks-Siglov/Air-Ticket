from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from flight.models import Flight


class DepartureFlightInline(admin.TabularInline):
    model = Flight
    fk_name = "departure_airport"
    extra = 0
    readonly_fields = (
        "number",
        "iata",
        "icao",
        "arrival_airport_link",
    )
    fields = (
        "number",
        "iata",
        "icao",
        "arrival_airport_link",
        "departure_scheduled",
        "arrival_scheduled",
    )
    verbose_name = "Departure Flight"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related(
            "arrival_airport",
        )

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def arrival_airport_link(self, obj):
        arrival_airport = obj.arrival_airport
        if arrival_airport:
            url = reverse(
                "admin:flight_airport_change", args=(arrival_airport.id,)
            )
            return format_html('<a href="{}">{}</a>', url, arrival_airport)
        else:
            return "-"

    arrival_airport_link.short_description = "Arrival Airport"
