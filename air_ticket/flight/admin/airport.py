from django.contrib import admin

from flight.admin.inlines import ArrivalFlightInline, DepartureFlightInline
from flight.models import Airport


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    inlines = (DepartureFlightInline, ArrivalFlightInline)
    list_display = ("name", "timezone", "iata", "icao")
    search_fields = ("name", "iata", "icao")
    list_filter = ("timezone",)
