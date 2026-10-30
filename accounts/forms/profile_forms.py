from django import forms

from hr_management.models import Team


class ProfileChangeRequestForm(forms.Form):

    CHANGE_TYPE_CHOICES = [
        ("", "Select what you would like to change"),
        ("Name", "Name"),
        ("Team", "Team"),
    ]

    change_type = forms.ChoiceField(
        label="What would you like to change?",
        choices=CHANGE_TYPE_CHOICES,
        widget=forms.Select(
            attrs={
                "id": "change_type",
            }
        ),
    )

    requested_first_name = forms.CharField(
        label="New First Name",
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "id": "requested_first_name",
            }
        ),
    )

    requested_last_name = forms.CharField(
        label="New Last Name",
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "id": "requested_last_name",
            }
        ),
    )

    requested_team = forms.ModelChoiceField(
        label="Requested Team",
        queryset=Team.objects.none(),
        required=False,
        empty_label="Select a team",
        widget=forms.Select(
            attrs={
                "id": "requested_team",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["requested_team"].queryset = (
            Team.objects
            .all()
            .order_by("name")
        )

    def clean(self):
        cleaned_data = super().clean()

        change_type = cleaned_data.get("change_type")

        first_name = cleaned_data.get(
            "requested_first_name",
            ""
        ).strip()

        last_name = cleaned_data.get(
            "requested_last_name",
            ""
        ).strip()

        requested_team = cleaned_data.get(
            "requested_team"
        )

        if change_type == "Name":
            if not first_name:
                self.add_error(
                    "requested_first_name",
                    "Please enter your new first name."
                )

            if not last_name:
                self.add_error(
                    "requested_last_name",
                    "Please enter your new last name."
                )

        if change_type == "Team":
            if requested_team is None:
                self.add_error(
                    "requested_team",
                    "Please select the team you would like to move to."
                )

        cleaned_data["requested_first_name"] = first_name
        cleaned_data["requested_last_name"] = last_name

        return cleaned_data