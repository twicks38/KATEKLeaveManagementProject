from django.db import transaction

from accounts.models import ProfileChangeRequest
from hr_management.models import TeamMembership


class ProfileRequestService:

    # ==================================================
    # Create profile change request
    # ==================================================

    @staticmethod
    @transaction.atomic
    def create_request(user, cleaned_data):

        change_type = cleaned_data["change_type"]

        existing_request = (
            ProfileChangeRequest.objects
            .filter(
                user=user,
                change_type=change_type,
                status="Pending"
            )
            .exists()
        )

        if existing_request:
            raise ValueError(
                f"You already have a pending "
                f"{change_type.lower()} change request."
            )

        if change_type == "Name":
            return ProfileChangeRequest.objects.create(
                user=user,
                change_type="Name",
                requested_first_name=(
                    cleaned_data["requested_first_name"]
                ),
                requested_last_name=(
                    cleaned_data["requested_last_name"]
                ),
            )

        if change_type == "Team":
            requested_team = cleaned_data["requested_team"]

            current_membership = (
                TeamMembership.objects
                .filter(
                    user=user,
                    active=True
                )
                .first()
            )

            if (
                current_membership
                and current_membership.team_id
                == requested_team.id
            ):
                raise ValueError(
                    "You are already assigned to this team."
                )

            return ProfileChangeRequest.objects.create(
                user=user,
                change_type="Team",
                requested_team=requested_team,
            )

        raise ValueError(
            "Invalid profile change request type."
        )