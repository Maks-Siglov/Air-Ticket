from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from flight.models import Flight


class ArrivalFlightInline(admin.TabularInline):
    model = Flight
    fk_name = "arrival_airport"
    extra = 0
    readonly_fields = (
        "number",
        "iata",
        "icao",
        "departure_airport_link",
    )
    fields = (
        "number",
        "iata",
        "icao",
        "departure_airport_link",
        "departure_scheduled",
        "arrival_scheduled",
    )
    verbose_name = "Arrival Flight"

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related(
            "departure_airport",
        )

    def has_delete_permission(self, request, obj=None) -> bool:
        return False

    def departure_airport_link(self, obj):
        departure_airport = obj.departure_airport
        if departure_airport:
            url = reverse(
                "admin:flight_airport_change", args=(departure_airport.id,)
            )
            return format_html('<a href="{}">{}</a>', url, departure_airport)
        else:
            return "-"

    departure_airport_link.short_description = "Departure Airport"
