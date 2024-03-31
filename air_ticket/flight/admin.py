from django.contrib import admin

from flight.models import Airplane, Flight


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


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
        "departure_scheduled",
    )
