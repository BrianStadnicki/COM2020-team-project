from .models import Bundle_posting, Reservation
import datetime as dt
from django.utils import timezone

BUNDLE_WEIGHT = 0.6 #kg

def get_sell_through(request):

    user = getattr(request, "user", None)

    if not getattr(user, "is_authenticated", False):
        return None
    
    if getattr(user, "user_type", None) != "seller":
        return None

    seller = user.seller

    collected = 0
    expired = 0
    total = 0

    bundles = Bundle_posting.objects.filter(seller=seller)

    for bundle in bundles:
        if bundle.status == "C":
            collected += 1
        elif bundle.status == "E":
            expired += 1
        total += 1

    no_show = 0
    reservations = Reservation.objects.filter(posting__seller=seller)

    for reservation in reservations:
        if reservation.status == "N":
            no_show += 1

    sell_through = f"{collected/total*100:.1f}%" if total else "0.0%"

    return {"collected": collected, "expired": expired, "no_show": no_show, "sell_through": sell_through}



def get_waste_proxy(request):
    
    user = getattr(request, "user", None)

    if not getattr(user, "is_authenticated", False):
        return None
    
    if getattr(user, "user_type", None) != "seller":
        return None
    
    seller = user.seller
    tz = timezone.get_current_timezone()

    reservations = Reservation.objects.filter(posting__seller=seller, is_collected=True).values_list("time_stamp", flat=True)

    total = reservations.count()

    week = 0
    cutoff = timezone.now() - dt.timedelta(days=7)

    for reservation in reservations:
        if reservation >= cutoff:
            week += 1

    return {"total": total*BUNDLE_WEIGHT, "week": week*BUNDLE_WEIGHT}



def get_best_pickup():
    pass



def get_best_categories():
    pass