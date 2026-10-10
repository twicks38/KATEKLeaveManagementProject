from . import views
from django.urls import path

app_name = 'leave_management'

urlpatterns = [
    path('', views.home, name='home'),
    path('leave-history/', views.user_leave_requests, name='leave_history'),
    path('calendar/', views.personal_calendar, name="personal_calendar")
]