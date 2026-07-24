from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


def login_page(request):
    return render(request, 'accounts/login_page.html')



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
