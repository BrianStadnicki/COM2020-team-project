from django.shortcuts import redirect

def seller_profile_handler(request):
    # Only run if user is logged in
    if request.user.is_authenticated:

        # Only care about sellers
        if request.user.user_type == "seller":

            # If seller profile does NOT exist → redirect
            if request.user.seller == None:
                return redirect("seller_extra")

    # Context processors must return a dict
    return {}