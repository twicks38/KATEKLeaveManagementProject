from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from leave_management.services.leave_service import LeaveCalculations
from leave_management.models import LeaveRequest
import calendar
from datetime import datetime, timedelta, date

# Create your views here.
@login_required
def home(request):
    user = request.user
    calculations = LeaveCalculations()

    context = {
        'days_taken': calculations.get_days_taken(user),
        'remaining_leave': calculations.get_remaining_leave(user),
        'pending_count': calculations.get_pending_leave_count(user),
        'upcoming_leave': calculations.get_upcoming_leave(user),
    }

    return render(request, 'home.html', context)


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

    return render(request, 'user_leave_history.html', context)


def personal_calendar(request):
    month = int(request.GET.get('month', datetime.today().month))
    year = int(request.GET.get('year', datetime.today().year))

    calendar_start = calendar.Calendar(firstweekday=calendar.SUNDAY)
    month_calendar = calendar_start.monthdayscalendar(year, month)

    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])

    user_requests = LeaveRequest.objects.filter(
        user = request.user,
        start_date__lte = last_day,
        end_date__gte = first_day,
    )

    request_days = {}

    for user_request in user_requests:
        current_day = user_request.start_date

        while current_day <= user_request.end_date:
            day_num = current_day.day

            if day_num not in request_days:
                request_days[day_num] = []

            request_days[day_num].append(user_request)

            current_day += timedelta(days=1)

    calendar_days = []

    for week in month_calendar:
        week_data = []

        for day in week:
            week_data.append({
                "day":day,
                "request_day": request_days.get(day, [])
            })

        calendar_days.append(week_data)

    prev_month = month-1
    prev_year = year

    if prev_month < 1:
        prev_month = 12
        prev_year -= 1

    next_month = month + 1
    next_year = year

    if next_month > 12:
        next_month = 1
        next_year += 1


    context = {
        "calendar_days": calendar_days,
        "month": month,
        "year": year,
        "month_name": calendar.month_name[month],
        "prev_month": prev_month,
        "prev_year": prev_year,
        "next_month": next_month,
        "next_year": next_year
    }

    return render(request, 'leave_management/calendar_page.html', context)