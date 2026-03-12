from django.shortcuts import redirect
from django.urls import reverse
from main.views import seller_profile


class SellerProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if request.user.is_authenticated:
            if request.user.user_type == "seller":
                if not hasattr(request.user, "seller"):
                    if request.path != reverse("seller_profile_view_url"):
                        return redirect("seller_profile_view_url")

        response = self.get_response(request)

        return response
