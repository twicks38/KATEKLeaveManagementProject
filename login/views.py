from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


def login_page(request):
    return render(request, 'login_site/login_page.html')



def authenticate_user(request):
    if request.method == 'POST':
        username = request.POST.get('pending')
        password = request.POST.get('pending')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('location pending')

        else: 
            messages.error(request, 'Invalid username or password.')

    return HttpResponseForbidden("Invalid request method")


def create_account(request):
    if request.method == 'POST':
        username = request.POST.get('pending')
        first_name = request.POST.get('pending')
        last_name = request.POST.get('pending')
        email = request.POST.get('pending')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('login_site:create_account')

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password)
        
        user.save()

        login(request, user)
        return redirect('locationpending')

    return render(request, 'login_site/create_account.html')