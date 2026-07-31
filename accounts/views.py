from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden, HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.


def login_page(request):
    return render(request, 'accounts/login_page.html')



def authenticate_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse("Pending redirection location")

        else: 
            messages.error(request, 'Invalid email address or password.')

    return HttpResponseForbidden("Invalid request method")
