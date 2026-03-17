from .models import Bundle_posting, Reservation
import datetime as dt
from django.utils import timezone
from collections import Counter

BUNDLE_WEIGHT = 0.6  # kg


def get_sell_through(seller, price_low, price_high):
    collected = 0
    expired = 0
    total = 0

    bundles = Bundle_posting.objects.filter(seller=seller, price__gte=price_low, price__lte=price_high)

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

    sell_through = f"{collected / total * 100:.1f}" if total else "0.0"

    return {
        "collected": collected,
        "expired": expired,
        "no_show": no_show,
        "sell_through": sell_through,
    }


def get_waste_proxy(seller):
    reservations = Reservation.objects.filter(
        posting__seller=seller, is_collected=True
    ).values_list("time_stamp", flat=True)

    total = reservations.count()

    week = 0
    cutoff = timezone.now() - dt.timedelta(days=7)

    for reservation in reservations:
        if reservation >= cutoff:
            week += 1

    return {
        "total": "{0:.2f}".format(total * BUNDLE_WEIGHT),
        "week": "{0:.2f}".format(week * BUNDLE_WEIGHT),
    }

def get_estimated_co2(consumer):
    reservations = Reservation.objects.filter(consumer=consumer, is_collected=True).all()

    co2 = 0.00

    for reservation in reservations:
        match reservation.posting.category.name:
            case "Meals":
                co2 += 10.20
            case "Bread & Pastries":
                co2 += 0.89
            case "Groceries":
                co2 += 3.45
            case "Flowers & Plants":
                co2 += 17.21
            case "Pet Food":
                co2 += 4.25
            case "Vegetarian":
                co2 += 0.76
            case "Vegan":
                co2 += 0.40
    
    return co2


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
            category_counter[bundle.category.name] += 1

    top_3 = category_counter.most_common(3)

    result = {}

    for i in range(3):
        if i < len(top_3):
            category = top_3[i][0]
            result[str(i)] = f"{category}"
        else:
            result[str(i)] = f"-"

    return result
