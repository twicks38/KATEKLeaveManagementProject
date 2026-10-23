from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import (
    authenticate, login, logout, update_session_auth_hash
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from hr_management.services.password_reset_service import PasswordResetService

# ==================================================
# Login Page
# ==================================================

def login_page(request):
    if request.user.is_authenticated:
        return redirect('leave_management:home')
    
    return render(request, 'accounts/login_page.html')

#stub first login data
def is_first_login(user):
        return user.profile.first_login

def authenticate_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if is_first_login(user):
                return redirect('accounts:change_password')
            return redirect('leave_management:home')

        messages.error(request, 'Invalid username or password.')
        return redirect('accounts:login')

    return HttpResponseForbidden("Invalid request method")

# ==================================================
# User Change Pass / Logout
# ==================================================

@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        user = request.user

        if not user.check_password(old_password):
            messages.error(request, 'Old password is incorrect.')
            return redirect('accounts:change_password')

        if new_password != confirm_password:
            messages.error(request, 'New passwords do not match.')
            return redirect('accounts:change_password')

        user.set_password(new_password)
        user.save()

        user.profile.first_login = False
        user.profile.save(
            update_fields=["first_login"]
        )

        update_session_auth_hash(request, user)

        messages.success(
            request,
            "Your password has been changed successfully."
        )

        return redirect('leave_management:home')

    return render(request, 'accounts/change_password.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('accounts:login')

# ==================================================
# Password Reset
# ==================================================

def forgot_password(request):
    return render(request, 'accounts/forgot_password.html')

def pass_reset_req(request):
    if request.method == "POST":
        username = request.POST.get("username")

        PasswordResetService.create_reset_request(
            username
        )

        messages.success(
            request,
            "If the username exists, a password reset request has been submitted."
        )

        return redirect("accounts:login")

    return redirect("accounts:forgot_password")