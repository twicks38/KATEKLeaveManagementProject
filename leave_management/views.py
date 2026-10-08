from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from leave_management.services.leave_service import LeaveCalculations
from leave_management.models import LeaveRequest
import calendar
from datetime import datetime, date

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

    return render(request, 'user_leave_history.html', context)
    


def personal_calendar(request):
    month = int(request.GET.get('month', datetime.today().month))
    year = int(request.GET.get('year', datetime.today().year))
 
    calendar_start = calendar.Calendar(firstweekday=calendar.SUNDAY)
    month_calendar = calendar_start.monthdatescalendar(year, month)
 
    first_day = datetime(year, month, 1).date()
    last_day = datetime(year, month, calendar.monthrange(year, month)[1]).date()
 
    user_requests = LeaveRequest.objects.filter(
        user = request.user,
        start_date__lte = last_day,
        end_date__gte = first_day,
        status__in=["Approved", "Pending"],
    ).order_by('start_date')

    calendar_weeks = []

    for week in month_calendar:
        week_start = week[0]
        week_end = week[-1]


        week_request = [
            leave_request
            for leave_request in user_requests
            if leave_request.start_date <= week_end and leave_request.end_date >= week_start
        ]

        days = []

        for current_day in week:
            days.append({
                "date":current_day,
                "day":current_day.day,
                "is_current_month":  current_day.month == month
            })

        leave_segments = []

        for leave_request in week_request:
            segment_start = max(leave_request.start_date,
                                week_start,
                                first_day
                )

            segment_end = min(
                leave_request.end_date,
                week_end,
                last_day
            )

            if segment_start >segment_end:
                continue

            start_column = (segment_start - week_start).days
            span = (segment_end - segment_start).days + 1

            leave_segments.append({
                "leave_request":leave_request,
                "start_column":start_column,
                "span": span,
                "end_column": start_column + span -1
            })


        lanes = []

        for segment in leave_segments:
            placed = False
            for lane_number, lane in enumerate(lanes):
                overlaps = False

                for exsiting_segment in lane:
                    if(segment["start_column"] <= exsiting_segment["end_column"]
                       and segment["end_column"] >= exsiting_segment["start_column"]):
                        overlaps = True
                        break

                if not overlaps:
                    lane.append(segment)
                    segment["lane"] = lane_number
                    placed = True
                    break

            if not placed:
                lanes.append([segment])
                segment["lane"] = len(lanes) - 1

        lane_count = max(len(lanes), 1)


        print("Week:", week_start, "to", week_end)
        print("Leave segments:", len(leave_segments))
        print("Segments:", leave_segments)



        calendar_weeks.append({
            "days":days,
            "leave_segments":leave_segments,
            "lane_count":lane_count
        })
    
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
        "calendar_weeks": calendar_weeks,
        "month": month,
        "year": year,
        "month_name": calendar.month_name[month],
        "prev_month": prev_month,
        "prev_year": prev_year,
        "next_month": next_month,
        "next_year": next_year
    }
    print("Leave requests found:", user_requests.count())
    return render(request, 'leave_management/calendar_page.html', context)