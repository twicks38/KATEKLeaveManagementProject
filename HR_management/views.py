from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from .services.password_reset_service import PasswordResetService
from .services.permission_service import PermissionService

# ==================================================
# HR dashboard
# ==================================================

@login_required
def hr_management(request):
    if not PermissionService.is_hr_user(request.user):
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
    if not PermissionService.is_hr_superuser(request.user):
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
    if not PermissionService.is_hr_superuser(request.user):
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
    if not PermissionService.is_hr_superuser(request.user):
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