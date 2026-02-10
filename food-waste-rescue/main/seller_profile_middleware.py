from django.shortcuts import redirect
from main.views import sellerExtra
      
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
                    
                    return sellerExtra(request)

        response = self.get_response(request)

        return response
