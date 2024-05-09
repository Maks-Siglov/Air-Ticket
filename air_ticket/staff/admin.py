from django.contrib import admin

from staff.models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("user", "role")
    filter = ("role",)

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser or (
            obj is not None and obj.user == request.user
        )

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser or (
            obj is not None and obj.user == request.user
        )

    def has_delete_permission(self, request, obj=None):
        return request.user
