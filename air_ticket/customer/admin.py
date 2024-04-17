from django.contrib import admin

from customer.models import Contact, Passenger


@admin.register(Passenger)
class PassengerAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "passport_id")
    search_fields = ("passport_id", "first_name", "last_name")
    ordering = ("passport_id",)


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "email", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
