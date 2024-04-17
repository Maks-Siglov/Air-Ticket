from django.contrib import admin

from customer.models import Passenger


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "passport_id")
    list_filter = ("created_at", "updated_at")
    search_fields = ("id", "passport_id", "first_name", "last_name")
