import secrets
import string

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.utils import timezone

from hr_management.models import PasswordResetRequest

class PasswordResetService:

    # ==================================================
    # Create password reset request
    # ==================================================

    @staticmethod
    def create_reset_request(username):
        user = User.objects.filter(
            username=username
        ).first()

        if not user:
            return

        PasswordResetRequest.objects.get_or_create(
            user=user,
            status="Pending",
        )


    # ==================================================
    # Retrieve pending requests
    # ==================================================

    @staticmethod
    def get_pending_requests():
        return (
            PasswordResetRequest.objects
            .filter(status="Pending")
            .select_related(
                "user",
                "user__profile",
            )
            .order_by("requested_at")
        )


    # ==================================================
    # Generate temporary password
    # ==================================================

    @staticmethod
    def generate_temporary_password(length=14):
        """
        Generate a random temporary password containing
        uppercase letters, lowercase letters, numbers
        and symbols.
        """

        uppercase_characters = string.ascii_uppercase
        lowercase_characters = string.ascii_lowercase
        number_characters = string.digits
        symbol_characters = "!@#$%&*?"

        all_characters = (
            uppercase_characters
            + lowercase_characters
            + number_characters
            + symbol_characters
        )

        password_characters = [
            secrets.choice(uppercase_characters),
            secrets.choice(lowercase_characters),
            secrets.choice(number_characters),
            secrets.choice(symbol_characters),
        ]

        password_characters.extend(
            secrets.choice(all_characters)
            for _ in range(length - 4)
        )

        secrets.SystemRandom().shuffle(
            password_characters
        )

        return "".join(password_characters)


    # ==================================================
    # Process password reset
    # ==================================================

    @staticmethod
    @transaction.atomic
    def process_reset_request(reset_id, processed_by):
        """
        Reset the user's password, mark the user's profile
        as requiring a password change, and complete the
        reset request.
        """

        try:
            password_request = (
                PasswordResetRequest.objects
                .select_for_update()
                .select_related("user")
                .get(
                    id=reset_id,
                    status="Pending",
                )
            )

        except PasswordResetRequest.DoesNotExist:
            raise ValueError(
                "This password reset request does not exist "
                "or has already been processed."
            )

        user = password_request.user

        try:
            profile = user.profile

        except ObjectDoesNotExist:
            raise ValueError(
                f"The user {user.username} does not have "
                f"a user profile."
            )

        temporary_password = (
            PasswordResetService.generate_temporary_password()
        )

        user.set_password(temporary_password)
        user.save(
            update_fields=["password"]
        )

        profile.first_login = True
        profile.save(
            update_fields=["first_login"]
        )

        password_request.status = "Completed"
        password_request.processed_by = processed_by
        password_request.processed_at = timezone.now()

        password_request.save(
            update_fields=[
                "status",
                "processed_by",
                "processed_at",
            ]
        )

        return {
            "username": user.username,
            "temporary_password": temporary_password,
        }


    # ==================================================
    # Reject password reset request
    # ==================================================

    @staticmethod
    @transaction.atomic
    def reject_request(reset_id, processed_by):
        """
        Reject a pending password reset request without
        changing the user's password.
        """

        try:
            password_request = (
                PasswordResetRequest.objects
                .select_for_update()
                .select_related("user")
                .get(
                    id=reset_id,
                    status="Pending",
                )
            )

        except PasswordResetRequest.DoesNotExist:
            raise ValueError(
                "This password reset request does not exist "
                "or has already been processed."
            )

        password_request.status = "Rejected"
        password_request.processed_by = processed_by
        password_request.processed_at = timezone.now()

        password_request.save(
            update_fields=[
                "status",
                "processed_by",
                "processed_at",
            ]
        )

        return password_request.user.username