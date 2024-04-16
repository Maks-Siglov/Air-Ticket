from django.contrib import admin

from flight.models import (
    Airplane,
    Airport,
    Flight
)


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ("name", "seats_amount")
    list_filter = ("seats_amount",)


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("name", "timezone", "iata", "icao")
    list_filter = ("timezone",)


@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "iata",
        "icao",
        "price",
        "lunch_price",
        "luggage_price",
        "airplane",
        "departure_airport",
        "arrival_airport",
        "departure_scheduled",
        "arrival_scheduled",
    )
    list_filter = (
        "departure_scheduled",
        "arrival_scheduled",
        "airplane",
        "departure_airport",
        "arrival_airport",
    )
    search_fields = ("number", "iata", "icao")
