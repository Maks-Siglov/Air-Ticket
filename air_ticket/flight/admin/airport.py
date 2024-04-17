from django.contrib import admin

from flight.models import Airport


@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ("name", "timezone", "iata", "icao")
    list_filter = ("timezone",)
