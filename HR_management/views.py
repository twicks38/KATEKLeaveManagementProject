from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Create your views here.
@login_required
def hr_management(request):
    if not request.user.groups.filter(name__in=["HR", "HR Superuser"]).exists():
        return HttpResponseForbidden("You do not have permission to access this page.")

    return render(request, 'hr_management/hr_dashboard.html')
