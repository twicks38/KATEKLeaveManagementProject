from . import views
from django.urls import path

app_name = 'hr_management'

urlpatterns = [
    path('', views.hr_management, name='hr_dashboard'),
]