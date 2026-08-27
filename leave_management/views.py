from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from leave_management.services.leave_service import LeaveCalculations
from leave_management.models import LeaveRequest

# Create your views here.
@login_required
def home(request):
    user = request.user
    calculations = LeaveCalculations()

    full_leave_history = LeaveRequest.objects.filter(user=user).order_by('-start_date')[:6]

    context = {
        'days_taken': calculations.get_days_taken(user),
        'remaining_leave': calculations.get_remaining_leave(user),
        'pending_count': calculations.get_pending_leave_count(user),
        'upcoming_leave': calculations.get_upcoming_leave(user),
        'full_leave_history': full_leave_history,
    }

    return render(request, 'accounts/home_page.html', context)


@login_required
def user_leave_requests(request):
    user = request.user

    full_leave_history = LeaveRequest.objects.filter(user=user).order_by('start_date')

    years = LeaveRequest.objects.filter(user=user).dates('start_date', 'year')

    selected_status = request.GET.get('status')
    selected_holiday_year = request.GET.get('holiday_year')
    selected_start = request.GET.get('start_date')
    selected_end = request.GET.get('end_date')

    if selected_status:
        full_leave_history = full_leave_history.filter(status=selected_status)

    if selected_holiday_year:
        full_leave_history = full_leave_history.filter(start_date__year=selected_holiday_year)

    if selected_start:
        full_leave_history = full_leave_history.filter(start_date__gte=selected_start)

    if selected_end:
        full_leave_history = full_leave_history.filter(end_date__lte=selected_end)

    context = {
        'full_leave_history': full_leave_history,
        'years': years,
        'selected_status': selected_status,
        'selected_holiday_year': selected_holiday_year,
        'selected_start': selected_start,
        'selected_end': selected_end,
    }

    return render(request, 'accounts/user_leave_history.html', context)