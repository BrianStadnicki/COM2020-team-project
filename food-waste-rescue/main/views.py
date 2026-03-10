from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .forms import (
    ReservationForm,
    SellerExtraForm,
    GenericSignupForm,
    BundleNewForm,
    IssueReportNewForm,
    IssueReportViewForm,
    ActionFormBundle,
    ActionFormAnalytics
)
from .models import Bundle_posting_category, User, Bundle_posting, Seller, Consumer, IssueReport, Reservation, Seller_actions
from .forecast_calc import avePerRes, avePerNoshow, errorMSEReservations, errorMSENoShow
from .badges import get_badges
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.forms.models import model_to_dict
import datetime
from .analytics import (
    get_best_categories,
    get_best_pickup,
    get_sell_through,
    get_waste_proxy,
)

"""
Consumer: Show all bundles, search by location and pick up time, pagination
Seller: Show own bundles, pagination
"""


@login_required
def bundles_view(request):
    # checks to see if the user is seller or consumer

    ALLERGENS = [
        "Celery",
        "Crustacean",
        "Dairy",
        "Egg",
        "Fish",
        "Gluten",
        "Lupin",
        "Mollusc",
        "Mustard",
        "Nut",
        "Peanut",
        "Sesame",
        "Soya",
        "Sulphite",
    ]

    if request.user.user_type != "seller":
        posts = Bundle_posting.objects
    else:
        posts = request.user.seller.bundle_posting_set

    location = request.GET.get("location", "")

    if request.user.user_type != "seller" and location:
        posts = posts.filter(seller__location__icontains=location)

    selected_category_id = request.GET.get("category", "")
    selected_category = ""
    
    selected_allergens = request.GET.getlist("excluded-allergens")

    if selected_category_id != "":
        selected_category = Bundle_posting_category.objects.get(id=selected_category_id)
        posts = posts.filter(category=selected_category)
    if selected_allergens:
        q = Q()
        for allergen in selected_allergens:
            field = f"allergen_{allergen.lower()}"
            q |= Q(**{field: True})
        posts = posts.exclude(q)

    posts = posts.order_by("-creation_time")
    posts = posts.all()

    return render(
        request,
        "main/bundles.html",
        {
            "posts": posts,
            "categories": Bundle_posting_category.objects.all(),
            "allergens": ALLERGENS,
            "selected_category": selected_category,
            "selected_allergens": selected_allergens,
            "selected-location": location,
        },
    )


"""
Consumer: Show bundle, make new reservation or view own reservation details
Seller: show/edit/delete bundle, change reservation status?
"""


@login_required
def bundle_view(request, id):
    post = get_object_or_404(Bundle_posting, pk=id)

    # Determining whether the logged-in user is a Seller: True = Seller, False = Consumer
    is_seller = (request.user.user_type == "seller") and (
        post.seller == request.user.seller
    )
    is_today = post.creation_time.date() == datetime.datetime.today().date()

    if request.method == "POST":
        if "submit_res" in request.POST:
            form = ReservationForm(request.POST)

            # Consumer makes a reservation
            if form.data["submit_res"] == "Reserve":
                reservation = Reservation(
                    posting=post,
                    consumer=Consumer.objects.get(user=request.user),
                    # claim_code generated in the reservation model method.
                )
                reservation.save()
                reservation.claim_code_generator()

            # Seller marks the reservation as collected
            elif form.data["submit_res"] == "Collected?":
                reservation = Reservation.objects.get(id=int(form.data["id"]))
                reservation.is_collected = True
                reservation.save()
        elif "submit_action" in request.POST:
            form = ActionFormBundle(request.POST)
            if form.is_valid():
                action = form.save(commit=False)
                action.seller = Seller.objects.get(user=request.user)
                action.category = post.category
                action.save()
                return redirect("bundle_view_url", id=post.id)

    if request.user.user_type == "consumer":
        reports = post.issuereport_set.filter(consumer=request.user.consumer).all()  # type: ignore
        reservations = post.reservation_set.filter(consumer=request.user.consumer).all()  # type: ignore
    else:
        reports = post.issuereport_set.all()  # type: ignore
        reservations = post.reservation_set.all()  # type: ignore

    return render(
        request,
        "main/bundle.html",
        {
            "post": post,
            "reports": reports,
            "reservations": reservations,
            "is_seller": is_seller,
            "is_today": is_today,
            "types": Seller_actions.TYPES
        },
    )


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
            if form.data["submit"] == "create":
                bundle = form.save(commit=False)
                bundle.seller_id = Seller.objects.get(user=request.user).id
                bundle.save()
                return redirect("bundle_view_url", id=bundle.id)
            else:
                bundle = form.save(commit=False)
                bundle.seller_id = Seller.objects.get(user=request.user).id
                form = BundleNewForm(None, initial=bundle.__dict__)
                form.initial["pickup_window_start"] = form.initial[
                    "pickup_window_start"
                ].__format__("%H:%M")
                form.initial["pickup_window_end"] = form.initial[
                    "pickup_window_end"
                ].__format__("%H:%M")
                form.initial["category"] = bundle.category.name

                exp_res = round(bundle.quantity * avePerRes(bundle.seller_id))
                exp_no_show = round(exp_res * avePerNoshow(bundle.seller_id))

                return render(
                    request,
                    "main/bundle_new.html",
                    {
                        "form": form,
                        "confirm": True,
                        "categories": Bundle_posting_category.objects.all(),
                        "exp_res": exp_res,
                        "exp_no_show": exp_no_show,
                    },
                )
    else:
        form = BundleNewForm()
    return render(
        request,
        "main/bundle_new.html",
        {
            "form": form,
            "categories": Bundle_posting_category.objects.all(),
            "confirm": False,
        },
    )


"""
Consumer: Show own reservations with bundle details
Seller: Show upcoming reservations with bundle details, edit status, search/verify code
"""

@login_required
def reservations_view(request):
    # checks to see if the user is seller or consumer
    if request.user.user_type != "seller":
        reservations = request.user.consumer.reservation_set
    else:
        reservations = request.user.seller.reservation_set

    location = request.GET.get("location", "")

    if request.user.user_type != "seller" and location:
        reservations = reservations.filter(seller__location__icontains=location)

    reservations = reservations.order_by("-time_stamp")
    reservations = reservations.all()

    return render(
        request,
        "main/reservations.html",
        {
            "reservations": reservations,
            "selected-location": location
        },
    )


"""
Consumer: Show own reservation with bundle details
Seller: Show own reservation with bundle details
"""


@login_required
def reservation_view(request, id):
    return render(request, "main/reservation.html")


"""
Seller: Show analytics
"""


@login_required
def analytics_view(request):
    if request.user.user_type != "seller":
        raise PermissionDenied

    seller = getattr(request, "user", None).seller

    sell_through = get_sell_through(seller)
    waste_proxy = get_waste_proxy(seller)
    best_pickup = get_best_pickup(seller)
    best_category = get_best_categories(seller)
    reservations_error = round(errorMSEReservations(seller), 2)
    reservations_no_show_error = round(errorMSENoShow(seller), 2)

    if request.method == "POST":
        form = ActionFormAnalytics(request.POST)
        if form.is_valid():
            action = form.save(commit=False)
            action.seller = Seller.objects.get(user=request.user)
            action.save()
            messages.success(request, "Action saved!")

    return render(
        request,
        "main/analytics.html",
        {
            "sell_through": sell_through,
            "waste_proxy": waste_proxy,
            "best_pickup": best_pickup,
            "best_category": best_category,
            "reservations_error": reservations_error,
            "reservations_no_show_error": reservations_no_show_error,
            "types": Seller_actions.TYPES,
            "categories": Bundle_posting_category.objects.all()
        },
    )


"""
Consumer: Show own reports
Seller: Show own reports
"""


@login_required
def reports_view(request):
    if request.user.user_type == "seller":
        reports = IssueReport.objects.filter(posting__seller=request.user.seller)
    else:
        reports = request.user.consumer.issuereport_set.all()

    selected_status = request.GET.get("status", "")
    selected_type = request.GET.get("type", "")

    if selected_status != "":
        reports = reports.filter(status=selected_status)
    if selected_type != "":
        reports = reports.filter(type=selected_type)

    return render(
        request,
        "main/reports.html",
        {
            "reports": reports,
            "selected_status": selected_status,
            "selected_type": selected_type,
        },
    )


"""
Consumer: Show/add/close own report
Seller: Show/add/close own report
"""


@login_required
def report_view(request, id):
    report = get_object_or_404(IssueReport, id=id)
    if request.user.user_type == "seller":
        if report.posting.seller_id != request.user.seller.id:
            raise PermissionDenied
    else:
        if report.consumer_id != request.user.consumer.id:
            raise PermissionDenied

    if request.method == "POST":
        form = IssueReportViewForm(request.POST or None, instance=report)
        if form.is_valid():
            report = form.save()
            return redirect("report_view_url", id=report.id)
    else:
        form = IssueReportViewForm(None, initial=report.__dict__)
    return render(
        request,
        "main/report_view.html",
        {"form": form, "edit": True, "bundle_id": report.posting.id},
    )


"""
Consumer: Create new report
"""


@login_required
def report_new_view(request, id):
    # Consumer-only page, so raising 403 Forbidden for Sellers
    if request.user.user_type == "seller":
        raise PermissionDenied
    # For Consumers:
    if request.method == "POST":
        form = IssueReportNewForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.posting_id = id
            report.consumer_id = Consumer.objects.get(user=request.user).id
            report.save()
            return redirect("report_view_url", id=report.id)
    else:
        form = IssueReportNewForm()
    return render(request, "main/report_new.html", {"form": form})


"""
Consumer: View impact
Seller: View impact
"""


@login_required
def impact_view(request):

    if request.user.user_type != "consumer":
        raise PermissionDenied

    consumer = getattr(request, "user", None).consumer

    badges = get_badges(consumer)

    return render(request, "main/impact.html", {"badges": badges})

@login_required
def action_view(request):

    if request.user.user_type != "seller":
        raise PermissionDenied
    
    seller = getattr(request, "user", None).seller

    actions = Seller_actions.objects.filter(seller=seller).order_by("-time_stamp")

    return render(request, "main/actions.html", {"actions":actions})

"""
Consumer: View/Change accessibility settings
Seller: View/Change accessibility settings
"""


@login_required
def accessibility_view(request):
    return render(request, "main/accessibility.html")


def seller_profile(request):
    if request.user.user_type != "seller":
        raise PermissionDenied
    
    if hasattr(request.user, "seller"):
        profile = request.user.seller
    else:
        profile = None
    
    if request.method == "POST":
        form = SellerExtraForm(request.POST or None, instance=profile)
        
        if form.is_valid():
            seller = form.save(commit=False)
            seller.user = request.user
            seller.save()
            form.save_m2m()
            messages.success(request, "Seller profile saved!")
            report = form.save()
            return redirect("seller_profile_view_url")
    elif profile != None:
        form = SellerExtraForm(None, initial=profile.__dict__)
        form.initial["opening_time"] = form.initial[
                    "opening_time"
                ].__format__("%H:%M")
        form.initial["closing_time"] = form.initial[
                    "closing_time"
                ].__format__("%H:%M")      
    else:
        form = SellerExtraForm()

    return render(
        request,
        "registration/seller_profile.html",
        {"form": form},
    )



########### register here #####################################
def registerUser(request):
    if request.user.is_authenticated:
        return redirect("/")  # TODO: Change to home page
    else:
        if request.method == "POST":
            form = GenericSignupForm(request.POST)
            if form.is_valid():
                user = form.save()  # returns custom user instance

                if user.user_type == "seller":
                    return redirect("login")
                else:
                    Consumer.objects.create(user=user)
                    messages.success(
                        request,
                        f"Your account has been created! You are now able to log in",
                    )
                    return redirect("login")
            else:
                messages.info(request, f"Check your details.")
                return render(
                    request,
                    "registration/signup.html",
                    {"form": form, "title": "register here"},
                )
        else:
            form = GenericSignupForm()
            return render(
                request,
                "registration/signup.html",
                {"form": form, "title": "register here"},
            )
