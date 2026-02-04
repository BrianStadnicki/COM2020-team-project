from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import SellerExtraForm, GenericSignupForm, BundleNewForm
from .models import User, Bundle_posting, Seller


def test_view(request):
    return render(request, "main/test.html")

"""
Consumer: Show all bundles, search by location and pick up time, pagination
Seller: Show own bundles, pagination
"""
def bundles_view(request):
    return render(request, "main/bundles.html")

"""
Consumer: Show bundle, make new reservation or view own reservation details
Seller: show/edit/delete bundle, change reservation status?
"""
def bundle_view(request, id):

    post = get_object_or_404(Bundle_posting, pk=id)

    return render(request, "main/bundle.html", {'post': post})

"""
Seller: create new bundle
"""
def bundle_new_view(request):
    if request.method == "POST":
        form = BundleNewForm(request.POST)
        if form.is_valid():
            bundle = form.save(commit=False)
            bundle.seller_id = Seller.objects.get(user = request.user).id
            bundle.save()
            return redirect("bundle_view_url", id = bundle.id)
    else:
        form = BundleNewForm()
    return render(request, "main/bundle_new.html", {"form": form, "edit": False})

"""
Seller: edit bundle
"""
def bundle_edit_view(request, id):
    bundle = get_object_or_404(Bundle_posting, id=id)
    if request.method == "POST":
        form = BundleNewForm(request.POST or None, instance=bundle)
        if form.is_valid():
            bundle = form.save()
            return redirect("bundle_view_url", id = bundle.id)
    else:
        form = BundleNewForm(None, initial=bundle.__dict__)
        form.initial["pickup_window_start"] = form.initial["pickup_window_start"].__format__("%H:%M")
        form.initial["pickup_window_end"] = form.initial["pickup_window_end"].__format__("%H:%M")

    return render(request, "main/bundle_new.html", {"form": form, "edit": True})

"""_
Seller: See analytics, actually create
"""
def bundle_confirm_view(request):
    return render(request, "main/bundle_confirm.html")

"""
Consumer: Show own reservations with bundle details
Seller: Show upcoming reservations with bundle details, edit status, search/verify code
"""
def reservations_view(request):
    return render(request, "main/reservations.html")

"""
Consumer: Show/delete own reservation with bundle details
Seller: Show/edit own reservation with bundle details
"""
def reservation_view(request, id):
    return render(request, "main/reservation.html")

"""
Seller: Show analytics
"""
def analytics_view(request):
    return render(request, "main/analytics.html")

"""
Consumer: Show own reports
Seller: Show own reports
"""
def reports_view(request):
    return render(request, "main/reports.html")

"""
Consumer: Show/add/close own report
Seller: Show/add/close own report
"""
def report_view(request, id):
    return render(request, "main/report.html")

"""
Consumer: Create new report
Seller: Create new report
"""
def report_new_view(request):
    return render(request, "main/report_new.html")

"""
Consumer: View impact
Seller: View impact
"""
def impact_view(request):
    return render(request, "main/impact.html")

"""
Consumer: View/Change accessibility settings
Seller: View/Change accessibility settings
"""
def accessibility_view(request):
    return render(request, "main/accessibility.html")

########### register here ##################################### 
def registerUser(request):
    if request.user.is_authenticated:
        return redirect("/") #TODO: Change to home page
    else:    
        if request.method == 'POST':
            form = GenericSignupForm(request.POST)
            if form.is_valid():
                user = form.save() #returns custom user instance

                if user.user_type == "seller":
                    return redirect("seller-extra", user_id=user.id)
                else:
                    #user = User.objects.create_user(form.cleaned_data.get("username"),form.cleaned_data("email"),form.cleaned_data("password1"),form.cleaned_data["user_type"],form.cleaned_data("password2")),
                    messages.success(request, f'Your account has been created! You are now able to log in')
                    return redirect("login")
            else:
                messages.info(request, f'Check your details.')
                form = GenericSignupForm()
                return render(request, 'registration/signup.html', {'form': form, 'title':'register here'})
        else:
            form = GenericSignupForm()
            return render(request, 'registration/signup.html', {'form': form, 'title':'register here'})
            


def sellerExtra(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        form = SellerExtraForm(request.POST)
        if form.is_valid():
            seller = form.save(commit=False)
            seller.user_id = user_id
            seller.save()
            form.save_m2m()
            messages.success(request, "Seller profile completed!")
            return redirect("login")
    else:
        form = SellerExtraForm()
    return render(request, "registration/seller_extra.html", {"form":form})
