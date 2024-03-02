from django.contrib import admin

from flight.models import Airplane, Flight, Seat


# @admin.register(Airplane)
# class AirplaneAdmin(admin.ModelAdmin):
#     list_display = ("name",)
#     search_fields = ("name",)
#
#
# @admin.register(Flight)
# class FlightAdmin(admin.ModelAdmin):
#     list_display = (
#         "airplane",
#         "departure_airport",
#         "destination_airport",
#         "departure_date",
#         "destination_date",
#     )
#     search_fields = (
#         "departure_airport",
#         "destination_airport",
#         "departure_date",
#     )
#
#
# @admin.register(Seat)
# class SeatAdmin(admin.ModelAdmin):
#     list_display = ("type", "airplane", "is_available")
#     list_filter = ("type", "is_available")
#     search_fields = ("type", "airplane__name")
