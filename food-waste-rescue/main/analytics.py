from .models import Bundle_posting, Reservation
import datetime as dt
from django.utils import timezone
from collections import Counter

BUNDLE_WEIGHT = 0.6 #kg

def get_sell_through(seller):

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



def get_waste_proxy(seller):

    reservations = Reservation.objects.filter(posting__seller=seller, is_collected=True).values_list("time_stamp", flat=True)

    total = reservations.count()

    week = 0
    cutoff = timezone.now() - dt.timedelta(days=7)

    for reservation in reservations:
        if reservation >= cutoff:
            week += 1

    return {"total": total*BUNDLE_WEIGHT, "week": week*BUNDLE_WEIGHT}



def get_best_pickup(seller):

    window_counter = Counter()

    bundles = Bundle_posting.objects.filter(seller=seller)
    
    for bundle in bundles:
        if bundle.status == "C":
            window = (bundle.pickup_window_start, bundle.pickup_window_end)
            window_counter[window] += 1

    top_3 = window_counter.most_common(3)

    result = {}

    for i in range(3):
        if i < len(top_3):
            start, end = top_3[i][0]
            result[str(i)] = f"{start.strftime('%H:%M')} - {end.strftime('%H:%M')}"
        else:
            result[str(i)] = f"-"

    return result


def get_best_categories(seller):

    category_counter = Counter()

    bundles = Bundle_posting.objects.filter(seller=seller)
    
    for bundle in bundles:
        if bundle.status == "C":
            category_counter[bundle.category] += 1

    top_3 = category_counter.most_common(3)

    result = {}

    for i in range(3):
        if i < len(top_3):
            category = top_3[i][0]
            result[str(i)] = f"{category}"
        else:
            result[str(i)] = f"-"

    return result