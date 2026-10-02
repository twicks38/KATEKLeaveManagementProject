from django.contrib import admin
from .models import LeaveRequest, SpecialLeaveType, Entitlement, AuditLog, Notification


@admin.register(SpecialLeaveType)
class SpecialLeaveTypeAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(Entitlement)
class EntitlementAdmin(admin.ModelAdmin):
    list_display = ("user", "holiday_year", "total_entitlement", "days_taken")
    list_filter = ("holiday_year",)
    search_fields = ("user__username", "user__email")
    ordering = ("holiday_year", "user__username")
    

@admin.register(LeaveRequest)
class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "leave_type",
        "special_leave_type",
        "start_date",
        "end_date",
        "status",
        "created_at",
        "approved_by",
    )
    list_filter = ("leave_type", "status", "start_date", "end_date")
    search_fields = ("user__username", "user__email", "leave_type")
    ordering = ("-created_at",)

    # Make LeaveRequest read-only in admin
    readonly_fields = (
        "user",
        "leave_type",
        "special_leave_type",
        "other_special_leave",
        "start_date",
        "end_date",
        "status",
        "created_at",
        "approved_by",
    )

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("action", "performed_by", "timestamp")
    search_fields = ("action", "performed_by__username")
    ordering = ("-timestamp",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "created", "read")
    list_filter = ("read",)
    search_fields = ("user__username", "message")
    ordering = ("-created",)

