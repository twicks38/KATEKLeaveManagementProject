from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from leave_management.services.leave_service import LeaveCalculations
from leave_management.models import LeaveRequest, SpecialLeaveType

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

@login_required
def leave_request_form(request):
    if request.method == "POST":
        leave_type = request.POST.get("leavetype")
        start_date = request.POST.get("startdate")
        end_date = request.POST.get("enddate")
        special_leave_reason = request.POST.get("special_leave_reason")
        special_leave_desc = request.POST.get("special_leave_desc")
        leave_request = LeaveRequest(user=request.user, leave_type=leave_type, start_date=start_date, end_date=end_date)

        if not start_date or not end_date:
            messages.error(request, "Please enter both a start date and an end date.")
            return render(request, 'accounts/leave_request_form.html')

        if start_date > end_date:
            messages.error(request, "The end date cannot be before the start date.")
            return render(request, 'accounts/leave_request_form.html')

        if leave_type == "Special":
            if not special_leave_reason:
                messages.error(request, "Please select a special leave reason.")
                return render(request, 'accounts/leave_request_form.html')

        if special_leave_reason == "Other" and not special_leave_desc:
            messages.error(request, "Please provide a description for Other special leave.")
            return render(request, 'accounts/leave_request_form.html')

        if leave_type == "Special":
            if special_leave_reason == "Other":
                leave_request.other_special_leave = special_leave_desc
            else:
                leave_request.special_leave_type = SpecialLeaveType.objects.get(name=special_leave_reason)

        leave_request.save()
        return redirect("leave_management:home")
    return render(request, 'accounts/leave_request_form.html')