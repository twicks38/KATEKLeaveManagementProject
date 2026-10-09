from django import forms

from leave_management.models import LeaveRequest, SpecialLeaveType
from leave_management.services.leave_service import LeaveCalculations

class LeaveRequestForm(forms.Form):
    LEAVE_TYPE_CHOICES = [
        ("Annual", "Annual Leave"),
        ("Special", "Special Leave"),
        ("Mat", "Maternity Leave"),
        ("Pat", "Paternity Leave"),
    ]

    leave_type = forms.ChoiceField(
        label="Type of Leave",
        choices=LEAVE_TYPE_CHOICES,
        widget=forms.Select(
            attrs={
                "id": "leave_type",
            }
        ),
    )

    start_date = forms.DateField(
        label="Start Date",
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
    )

    end_date = forms.DateField(
        label="End Date",
        widget=forms.DateInput(
            attrs={
                "type": "date",
            }
        ),
    )

    special_leave_reason = forms.ModelChoiceField(
        label="Special Leave Reason",
        queryset=SpecialLeaveType.objects.none(),
        required=False,
        empty_label="Select a reason",
        widget=forms.Select(
            attrs={
                "id": "special_leave_reason",
            }
        ),
    )

    special_leave_description = forms.CharField(
        label="Special Leave Description",
        required=False,
        widget=forms.Textarea(
            attrs={
                "id": "special_leave_description",
                "rows": 4,
                "placeholder": "Please describe the reason for your leave",
            }
        ),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = user

        self.fields["special_leave_reason"].queryset = (
            SpecialLeaveType.objects.all().order_by("name")
        )

    def clean(self):
        # Validate the form data and add custom validation logic
        cleaned_data = super().clean()

        leave_type = cleaned_data.get("leave_type")
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        special_leave_reason = cleaned_data.get("special_leave_reason")
        special_leave_description = cleaned_data.get(
            "special_leave_description",
            "",
        ).strip()

        # Validate that the end date is not before the start date
        if start_date and end_date and start_date > end_date:
            self.add_error(
                "end_date",
                "The end date cannot be before the start date.",
            )

        # Validate special leave reason and description
        if leave_type == "Special":
            if special_leave_reason is None:
                self.add_error(
                    "special_leave_reason",
                    "Please select a special leave reason.",
                )

            elif (
                special_leave_reason.name == "Other"
                and not special_leave_description
            ):
                self.add_error(
                    "special_leave_description",
                    "Please provide a description for other special leave.",
                )

        # Validate overlapping leave requests (So users cannot request leave for dates they already have leave)
        if start_date and end_date:
            overlapping_leave = LeaveRequest.objects.filter(
                user=self.user,
                start_date__lte=end_date,
                end_date__gte=start_date
            ).exists()

            if overlapping_leave:
                self.add_error(
                    None,
                    "You already have a leave request for some of these dates."
                )

        # Validate remaining leave for Annual Leave (So users cannot request more days than they have left)
        if (
            leave_type == "Annual"
            and start_date
            and end_date
        ):
            calculations = LeaveCalculations()

            requested_days = calculations.calculate_days_taken(
                start_date,
                end_date
            )

            remaining_days = calculations.get_remaining_leave(
                self.user
            )

            if requested_days > remaining_days:
                self.add_error(
                    "end_date",
                    f"You only have {remaining_days} days remaining."
                )

        cleaned_data["special_leave_description"] = (
            special_leave_description
        )

        return cleaned_data