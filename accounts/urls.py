from . import views
from django.urls import path

app_name = 'accounts'

urlpatterns = [

    # Login/Logout Authentication
    path('login/', views.login_page, name='login'),
    path('login/authenticate/', views.authenticate_user, name='user_authenticate'),
    path('logout/', views.user_logout, name='user_logout'),

    # Passwords
    path('change_password/', views.change_password, name = 'change_password'),
    path('forgot_password/', views.forgot_password, name = 'forgot_password'),
    path("password-reset-request/", views.pass_reset_req,name="pass_reset_req"),

    # User Profile
    path("profile/", views.profile, name="profile"),
    path("profile/personal-details/", views.personal_details, name="personal_details"),
    path("profile/employment/", views.employment_details, name="employment_details"),
    path("profile/leave/", views.leave_details, name="leave_details"),
    path("profile/requests/", views.profile_requests, name="profile_requests"),
    path("profile/request-change/", views.request_profile_change, name="request_profile_change"),
]