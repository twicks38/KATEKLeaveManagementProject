from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    job_title = models.CharField(max_length=255)

    first_login = models.BooleanField(default=True)

    start_date = models.DateField()

    working_days = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user.username} - {self.job_title}"

# ==================================================
# Profile change request
# ==================================================

class ProfileChangeRequest(models.Model):

    CHANGE_TYPE_CHOICES = [
        ("Name", "Name Change"),
        ("Team", "Team Change"),
    ]

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="profile_change_requests"
    )

    change_type = models.CharField(
        max_length=20,
        choices=CHANGE_TYPE_CHOICES
    )

    requested_first_name = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )

    requested_last_name = models.CharField(
        max_length=150,
        null=True,
        blank=True
    )

    requested_team = models.ForeignKey(
        "hr_management.Team",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profile_change_requests"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Pending"
    )

    requested_at = models.DateTimeField(
        auto_now_add=True
    )

    processed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="processed_profile_change_requests"
    )

    processed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return (
            f"{self.user.username} - "
            f"{self.change_type} - "
            f"{self.status}"
        )