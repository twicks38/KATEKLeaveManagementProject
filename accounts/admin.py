from django.contrib import admin
from .models import UserProfile
# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "job_title", "start_date", "working_days", "first_login")
    list_filter = ("job_title", "first_login")
    search_fields = ("user__username", "user__email", "job_title")
    ordering = ("user__username",)