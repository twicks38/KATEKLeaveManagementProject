from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from .services.password_reset_service import PasswordResetService
from .services.permission_service import PermissionService as Perms
from .services.profile_change_service import ProfileChangeService

# ==================================================
# HR dashboard
# ==================================================

@login_required
def hr_management(request):
    if not Perms.is_hr_user(request.user):
        return HttpResponseForbidden(
            "You do not have permission to access this page."
        )

    return render(
        request,
        "hr_management/hr_dashboard.html",
    )


# ==================================================
# Password reset request list
# ==================================================

@login_required
def password_reset_requests(request):
    if not Perms.is_hr_superuser(request.user):
        return HttpResponseForbidden(
            "You do not have permission to view password reset requests."
        )

    context = {
        "password_reset_requests": (
            PasswordResetService.get_pending_requests()
        ),
    }

    return render(
        request,
        "hr_management/password_requests.html",
        context,
    )


# ==================================================
# Process password reset
# ==================================================

@login_required
@require_POST
def reset_user_password(request, reset_id):
    if not Perms.is_hr_superuser(request.user):
        return HttpResponseForbidden(
            "You do not have permission to reset passwords."
        )

    try:
        result = PasswordResetService.process_reset_request(
            reset_id=reset_id,
            processed_by=request.user,
        )

        messages.success(
            request,
            (
                f"Password reset completed for "
                f"{result['username']}. "
                f"Temporary password: "
                f"{result['temporary_password']}"
            ),
        )

    except ValueError as error:
        messages.error(
            request,
            str(error),
        )

    return redirect(
        "hr_management:password_reset_requests"
    )


# ==================================================
# Reject password reset request
# ==================================================

@login_required
@require_POST
def reject_password_reset(request, reset_id):
    if not Perms.is_hr_superuser(request.user):
        return HttpResponseForbidden(
            "You do not have permission to reject password reset requests."
        )

    try:
        username = PasswordResetService.reject_request(
            reset_id=reset_id,
            processed_by=request.user,
        )

        messages.success(
            request,
            (
                f"The password reset request for "
                f"{username} was rejected."
            ),
        )

    except ValueError as error:
        messages.error(
            request,
            str(error),
        )

    return redirect(
        "hr_management:password_reset_requests"
    )

# ==================================================
# Profile change requests
# ==================================================

@login_required
def profile_change_requests(request):
    if not Perms.is_hr_user(request.user):
        return HttpResponseForbidden(
            "You do not have permission to view "
            "profile change requests."
        )

    context = {
        "profile_change_requests":
            ProfileChangeService.get_pending_requests(),
    }

    return render(
        request,
        "hr_management/profile_change_requests.html",
        context,
    )


# ==================================================
# Approve profile change
# ==================================================

@login_required
@require_POST
def approve_profile_change(request, request_id):
    if not Perms.is_hr_user(request.user):
        return HttpResponseForbidden(
            "You do not have permission to approve "
            "profile change requests."
        )

    try:
        change_request = (
            ProfileChangeService.approve_request(
                request_id=request_id,
                processed_by=request.user,
            )
        )

        messages.success(
            request,
            (
                f"{change_request.change_type} change "
                f"approved for "
                f"{change_request.user.username}."
            ),
        )

    except ValueError as error:
        messages.error(
            request,
            str(error),
        )

    return redirect(
        "hr_management:profile_change_requests"
    )


# ==================================================
# Reject profile change
# ==================================================

@login_required
@require_POST
def reject_profile_change(request, request_id):
    if not Perms.is_hr_user(request.user):
        return HttpResponseForbidden(
            "You do not have permission to reject "
            "profile change requests."
        )

    try:
        change_request = (
            ProfileChangeService.reject_request(
                request_id=request_id,
                processed_by=request.user,
            )
        )

        messages.success(
            request,
            (
                f"{change_request.change_type} change "
                f"rejected for "
                f"{change_request.user.username}."
            ),
        )

    except ValueError as error:
        messages.error(
            request,
            str(error),
        )

    return redirect(
        "hr_management:profile_change_requests"
    )