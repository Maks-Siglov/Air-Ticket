from django.contrib import admin

from flight.models import Airplane


@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ("name", "seats_amount")
    list_filter = ("seats_amount",)
