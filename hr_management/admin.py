from django.contrib import admin
from .models import Team, TeamMembership

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(TeamMembership)
class TeamMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "team", "role", "date_joined", "active")
    list_filter = ("team", "role", "active")
    search_fields = ("user__username", "user__email", "team__name", "role__name")
    ordering = ("team", "user__username")

