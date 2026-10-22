from . import views
from django.urls import path

app_name = 'hr_management'

urlpatterns = [
    path('', views.hr_management, name='hr_dashboard'),
    path('passwords_requests', views.password_reset_requests, name='password_reset_requests'),
    path(
        "password-reset-requests/<int:reset_id>/reset/",
        views.reset_user_password,
        name="reset_user_password"
    ),
    path(
        "password-reset-requests/<int:reset_id>/reject/",
        views.reject_password_reset,
        name="reject_password_reset"
    ),
]