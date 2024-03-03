from django.contrib import admin

from flight.models import Airplane, Flight, Seat


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("type", "airplane", "is_available")
    list_filter = ("type", "is_available")
    search_fields = ("type", "airplane__name")


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "iata",
        "icao",
        "airplane",
        "departure_airport",
        "arrival_airport",
        "arrival_scheduled",
        "departure_scheduled"
    )
