from . import views
from django.urls import path

app_name = 'login_site'

urlpatterns = [
    path('', views.login_page, name='login'),
    path('authenticate/', views.authenticate_user, name='user_authenticate'),
    path('create-account/', views.create_account, name='create_account'),
]