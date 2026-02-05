from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .forms import ReservationForm, SellerExtraForm, GenericSignupForm, BundleNewForm, IssueReportNewForm, IssueReportViewForm
from .models import User, Bundle_posting, Seller, Consumer, IssueReport, Reservation
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

def test_view(request):
    return render(request, "main/test.html")

"""
Consumer: Show all bundles, search by location and pick up time, pagination
Seller: Show own bundles, pagination
"""
@login_required
def bundles_view(request):

    ALLERGENS = [
    "Celery", "Crustacean", "Dairy", "Egg", "Fish", "Gluten", "Lupin",
    "Mollusc", "Mustard", "Nut", "Peanut", "Sesame", "Soya", "Sulphite"
    ]

    posts = Bundle_posting.objects.all()

    selected_category = request.GET.get("category", "")
    selected_allergens = request.GET.getlist("excluded-allergens")

    if selected_category and selected_category != "Select category":
        posts = posts.filter(category=selected_category)
    if selected_allergens:
        q=Q()
        for allergen in selected_allergens:
            field = f"allergen_{allergen.lower()}"
            q |= Q(**{field: True})
        posts = posts.exclude(q)

    categories = Bundle_posting.objects.values_list('category', flat=True).distinct()

    return render(request, "main/bundles.html", {'posts': posts, 'categories': categories, 'allergens': ALLERGENS,
                                                  "selected_category": selected_category, "selected_allergens":selected_allergens})

"""
Consumer: Show bundle, make new reservation or view own reservation details
Seller: show/edit/delete bundle, change reservation status?
"""
@login_required
def bundle_view(request, id):
    post = get_object_or_404(Bundle_posting, pk=id)
    
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.data["status"] == "create":
            reservation = Reservation(
                posting = post,
                consumer = Consumer.objects.get(user = request.user),
                claim_code = 1000
            )
            reservation.save()
        elif form.data["status"] == "collected":
            reservation = Reservation.objects.get(id=int(form.data["id"]))
            reservation.status = "C"
            reservation.save()

    reports = post.issuereport_set.all() # type: ignore

    for report in reports:
        for status in report.STATUSES:
            if status[0] == report.status:
                report.status = status[1]
        for type in report.TYPES:
            if (type[0] == report.type):
                report.type = type[1]

    reservations = post.reservation_set.all() # type: ignore
    
    for reservation in reservations:
        for status in reservation.STATUSES:
            if status[0] == reservation.status:
                reservation.status = status[1]

    return render(request, "main/bundle.html", {'post': post, 'reports': reports, 'reservations': reservations})

"""
Seller: create new bundle
"""
@login_required
def bundle_new_view(request):
    if request.user.user_type != "seller":
        raise PermissionDenied
    if request.method == "POST":
        form = BundleNewForm(request.POST)
        if form.is_valid():
            bundle = form.save(commit=False)
            bundle.seller_id = Seller.objects.get(user = request.user).id
            bundle.save()
            return redirect("bundle_view_url", id=bundle.id)
    else:
        form = BundleNewForm()
    return render(request, "main/bundle_new.html", {"form": form, "edit": False})

"""
Seller: edit bundle
"""
@login_required
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
@login_required
def bundle_confirm_view(request):
    return render(request, "main/bundle_confirm.html")

"""
Consumer: Show own reservations with bundle details
Seller: Show upcoming reservations with bundle details, edit status, search/verify code
"""
@login_required
def reservations_view(request):
    return render(request, "main/reservations.html")

"""
Consumer: Show/delete own reservation with bundle details
Seller: Show/edit own reservation with bundle details
"""
@login_required
def reservation_view(request, id):
    return render(request, "main/reservation.html")

"""
Seller: Show analytics
"""
@login_required
def analytics_view(request):
    return render(request, "main/analytics.html")

"""
Consumer: Show own reports
Seller: Show own reports
"""
@login_required
def reports_view(request):
    selected_status = request.GET.get("status", "")
    selected_type = request.GET.get("type", "")

    reports = IssueReport.objects.all()

    if selected_status != "":
        reports = reports.filter(status=selected_status)
    if selected_type != "":
        reports = reports.filter(type=selected_type)
    
    for report in reports:
        for status in report.STATUSES:
            if status[0] == report.status:
                report.status = status[1]
        for type in report.TYPES:
            if (type[0] == report.type):
                report.type = type[1]
    
    return render(request, "main/reports.html", {'reports': reports, "selected_status": selected_status, "selected_type": selected_type})


"""
Consumer: Show/add/close own report
Seller: Show/add/close own report
"""
@login_required
def report_view(request, id):
    report = get_object_or_404(IssueReport, id=id)
    if request.method =="POST":
        form = IssueReportViewForm(request.POST or None, instance = report)
        if form.is_valid() :
            report = form.save()
            return redirect("report_view_url", id=report.id)
    else:
        form = IssueReportViewForm(None, initial=report.__dict__)
    return render(request, "main/report_view.html", {"form" : form, "edit" : True, "bundle_id": report.posting.id})

"""
Consumer: Create new report
Seller: Create new report
"""
@login_required
def report_new_view(request, id):
    if request.method == "POST":
        form = IssueReportNewForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.posting_id = id
            report.consumer_id = Consumer.objects.get(user = request.user).id
            report.save()
            return redirect("report_view_url", id=report.id)
    else:
        form = IssueReportNewForm()
    return render(request, "main/report_new.html", {'form': form })

"""
Consumer: View impact
Seller: View impact
"""
@login_required
def impact_view(request):
    return render(request, "main/impact.html")

"""
Consumer: View/Change accessibility settings
Seller: View/Change accessibility settings
"""
@login_required
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
                    Consumer.objects.create(user = user)
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
    if user.user_type != "seller":
        raise PermissionDenied
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

