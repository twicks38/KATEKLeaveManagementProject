from datetime import timedelta, date
from django.utils import timezone
from leave_management.models import LeaveRequest, Entitlement

class LeaveCalculations:
    def calculate_days_taken(self, start_date, end_date):
        days_taken = 0
        current_day = start_date
        while current_day <= end_date:
            if current_day.weekday() <5:
                days_taken += 1
            current_day += timedelta(days=1)
        return days_taken

    def get_days_taken(self, user):
        current_year = date.today().year
        approved_leave = LeaveRequest.objects.filter(user=user, leave_type='Annual', status='Approved', start_date__year=current_year)
        total_days = 0
        for leave in approved_leave:
            total_days += self.calculate_days_taken(leave.start_date, leave.end_date)
        return total_days

    def get_remaining_leave(self, user):
        current_year = date.today().year
        entitlement_record = Entitlement.objects.get(user=user, holiday_year=current_year)
        remaining_leave = entitlement_record.total_entitlement - entitlement_record.days_taken
        return remaining_leave

    def get_pending_leave_count(self, user):
        return LeaveRequest.objects.filter(user=user, status='Pending').count()

    def get_upcoming_leave(self, user):
        today = date.today()
        return LeaveRequest.objects.filter(user=user, start_date__gte=today).order_by('start_date')[:6]
    
