from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('login/authenticate/', views.authenticate_user, name='user_authenticate'),
    path('change_password/', views.change_password, name = 'change_password'),
    path('logout/', views.user_logout, name='user_logout'),
    path('forgot_password/', views.forgot_password, name = 'forgot_password'),
    path("password-reset-request/", views.pass_reset_req,name="pass_reset_req")
]