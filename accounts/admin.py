from django.contrib import admin
from .models import UserProfile
from HR_management.models import TeamMembership
# Register your models here.

#inline for TeamMembership to be displayed in the UserProfile admin page to allow for team allocation at the same time as creating a new user
#It shows one empty row for team allocation and allows for only one team to be allocated to a user at a time.
class TeamMembershipInline(admin.TabularInline):
    model = TeamMembership
    extra = 1
    max_num = 1

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "job_title", "start_date", "working_days", "first_login")
    list_filter = ("job_title", "first_login")
    search_fields = ("user__username", "user__email", "job_title")
    ordering = ("user__username",)
    inlines = [TeamMembershipInline]