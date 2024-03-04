from django.contrib import admin
from customer.models import Passenger


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ("passport_id", "first_name", "last_name", "email")
    search_fields = ("passport_id", "first_name", "last_name", "email")
    ordering = ("passport_id",)
