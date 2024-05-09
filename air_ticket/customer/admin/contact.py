from django.contrib import admin

from customer.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "phone_number", "email", "created_at", "updated_at")
    list_filter = ("created_at", "updated_at")
    search_fields = ("id", "phone_number", "email")
