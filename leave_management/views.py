from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from leave_management.models import LeaveRequest

# Create your views here.
@login_required

def home(request):
    user = request.user


#This is to calculate the number of days taken for approved annual leave.
#First it filters for the leave requests of the logged in user for type 'Annual' and status 'Approved'
    approved_leave = LeaveRequest.objects.filter(
        user=user,
        leave_type='Annual',
        status='Approved'
    )

#This calculate the number of days between the start and end date of each approved leave request 
#+1 is added to include both the start and end date in the count
#if and added to ensure both start and end dates are present to avoid calculation errors. 
    days_taken = sum((request.end_date - request.start_date).days + 1 for request in approved_leave 
                 if request.end_date and request.start_date
                 )


    entitlment = user.profile.leave_entitlement
    remaining_leave = entitlment - days_taken

    pending_count = LeaveRequest.objects.filter(
        user = user,
        status = 'Pending'
    ).count()

#This is to get the upcoming leave requests of the logged in user
#It filters for start date that is on or after the current date and orders them by start date
#Results are limited to the first 6 upcomimg requests to avoid overwhelming the display
    today = timezone.now().date()

    upcoming_leave = LeaveRequest.objects.filter(
        user=user,
        start_date__gte=today
    ).order_by('start_date')[:6]

#This dictionary is used to pass the calculated values to the template to allow dynamic rending of users information on the home page
    context = {
        'days_taken': days_taken,
        'remaining_leave': remaining_leave,
        'pending_count': pending_count,
        'upcoming_leave': upcoming_leave,

    }

    return render(request, 'home.html', context)