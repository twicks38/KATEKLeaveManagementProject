from django.db import models
from django.contrib.auth.models import User

#This model stores the leave requests made by the user


class LeaveRequest (models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leave_requests")
    start_date = models.DateField()
    end_date = models.DateField()

    LEAVE_TYPES = [
        ("Annual", "Annual Leave"),
        ("Special", "Special Leave"),
        ("Mat", "Maternity Leave"),
        ("Pat", "Paternity Leave"),
    ]
    leave_type = models.CharField(choices=LEAVE_TYPES)

    special_leave_type = models.ForeignKey('SpecialLeaveType', on_delete=models.SET_NULL, null=True, blank=True, related_name='special_leave_requests')
    other_special_leave = models.CharField(max_length=255, null=True, blank=True)

    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]
    status = models.CharField(choices=STATUS_CHOICES, default="Pending")

    created_at = models.DateTimeField(auto_now_add=True)

    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="approved_leave_requests")

    def __str__(self):
        return f"{self.user.username} - {self.leave_type} ({self.start_date} to {self.end_date})"

class SpecialLeaveType(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name}"

class Entitlement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    holiday_year = models.IntegerField()
    total_entitlement = models.DecimalField(max_digits=5, decimal_places=2)
    days_taken = models.DecimalField(max_digits=5, decimal_places=1, default=0)


class AuditLog(models.Model):
    id = models.AutoField(primary_key=True)
    action = models.CharField(max_length=255)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} by {self.performed_by.username} at {self.timestamp}"

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"


