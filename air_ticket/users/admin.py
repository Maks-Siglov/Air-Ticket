from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "email",
        "phone_number",
        "created_at",
        "updated_at",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("created_at", "is_staff", "is_superuser", "is_active")
    search_fields = ("email", "phone_number")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("created_at", "updated_at")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
    ordering = ("email",)
