from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile

# Create your views here.


def login_page(request):
    return render(request, 'accounts/login_page.html')

def change_password(request):
    return render(request, 'accounts/change_password.html')

def home_page(request):
    return render(request, 'accounts/home_page.html')


#stub first login data
def is_first_login(user):
        return True

def authenticate_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if is_first_login(user):
                return redirect('accounts:change_password')
            return redirect('accounts:home_page')

        messages.error(request, 'Invalid username or password.')
        return redirect('accounts:login')

    return HttpResponseForbidden("Invalid request method")

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

        return redirect('accounts:home_page')

    return render(request, 'accounts/change_password.html')