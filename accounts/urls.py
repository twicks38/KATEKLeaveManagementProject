from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('login/authenticate/', views.authenticate_user, name='user_authenticate'),
]