from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=255)
    annual_leave = models.IntegerField()
    first_login = models.BooleanField(default=True)
def __str__(self):
    return f"{self.user.username} - {self.job_title}"

