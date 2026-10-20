from datetime import date
from leave_management.models import LeaveRequest, Entitlement
from django.db import transaction
from .util import calculate_working_days
from .entitlement_service import EntitlementCalculations

class LeaveCalculations:

    def calculate_days_taken(self, start_date, end_date):
        return calculate_working_days(start_date, end_date)

    def get_days_taken(self, user, holiday_year=None):
        if holiday_year is None:
            holiday_year = date.today().year

        year_start = date(holiday_year, 1, 1)
        year_end = date(holiday_year, 12, 31)

        approved_leave = LeaveRequest.objects.filter(
            user=user,
            leave_type="Annual",
            status="Approved",

            # The request must overlap this holiday year
            start_date__lte=year_end,
            end_date__gte=year_start
        )

        total_days = 0

        for leave in approved_leave:
            # Keep only the part of the request inside this year
            calculation_start = max(
                leave.start_date,
                year_start
            )

            calculation_end = min(
                leave.end_date,
                year_end
            )

            total_days += self.calculate_days_taken(
                calculation_start,
                calculation_end
            )

        return total_days
    
    def get_remaining_leave(self, user):
        current_year = date.today().year

        entitlement_calculations = EntitlementCalculations()

        entitlement_record = (
            entitlement_calculations.check_entitlement_record(user)
        )

        days_taken = self.get_days_taken(
            user,
            holiday_year=current_year
        )

        return (
            entitlement_record.total_entitlement
            - days_taken
        )

    def get_pending_leave_count(self, user):
        return LeaveRequest.objects.filter(
            user=user,
            status="Pending"
        ).count()

    def get_upcoming_leave(self, user):
        today = date.today()

        return LeaveRequest.objects.filter(
            user=user,
            start_date__gte=today
        ).order_by("start_date")[:6]
  
class LeaveRequestService:

    @staticmethod
    @transaction.atomic # DjangoDB feature that ensures either all operations succeed or none do.
    def create_leave_request(user, cleaned_data):

        leave_request = LeaveRequest(
            user=user,
            leave_type=cleaned_data["leave_type"],
            start_date=cleaned_data["start_date"],
            end_date=cleaned_data["end_date"],
        )

        special_leave_reason = cleaned_data.get(
            "special_leave_reason"
        )

        special_leave_description = cleaned_data.get(
            "special_leave_description"
        )

        if cleaned_data["leave_type"] == "Special":

            if (
                special_leave_reason
                and special_leave_reason.name == "Other"
            ):
                leave_request.other_special_leave = (
                    special_leave_description
                )

            else:
                leave_request.special_leave_type = (
                    special_leave_reason
                )

        leave_request.save()

        return leave_request