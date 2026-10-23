from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.urls import reverse


class ForcePasswordChangeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:

            change_password_url = reverse(
                "accounts:change_password"
            )

            logout_url = reverse(
                "accounts:user_logout"
            )

            allowed_urls = [
                change_password_url,
                logout_url,
            ]

            if request.path not in allowed_urls:

                try:
                    if request.user.profile.first_login:
                        return redirect(
                            "accounts:change_password"
                        )

                except ObjectDoesNotExist:
                    pass

        return self.get_response(request)
