from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "status")
    list_filter = ("status",)
    search_fields = ("id", "flight__number", "status")
    ordering = ("-id",)
