# Contains for forecast
from .models import Bundle_posting, Seller, Reservation
from django.db.models import Sum, Count, F
from django.db import models
from django.utils import timezone
from datetime import time, datetime, timedelta
from sklearn.metrics import mean_squared_error


""" Fetch the Sellers Bundle Reservation from between 3 and 6 weeks ago
    and calculate average percentage number of reservations."""


def avePerRes(seller_id):
    recent_postings = Bundle_posting.objects.filter(seller_id=seller_id)
    recent_postings = recent_postings.filter(
        creation_time__lte=timezone.now() - timedelta(weeks=3)
    )
    recent_postings = recent_postings.filter(
        creation_time__gte=timezone.now() - timedelta(weeks=6)
    )
    recent_postings_quantity_count = recent_postings.aggregate(Sum("quantity"))[
        "quantity__sum"
    ]
    recent_reservations_count = Reservation.objects.filter(posting__seller_id=seller_id)
    recent_reservations_count = recent_reservations_count.filter(
        time_stamp__lte=timezone.now() - timedelta(weeks=3)
    )
    recent_reservations_count = recent_reservations_count.filter(
        time_stamp__gte=timezone.now() - timedelta(weeks=6)
    ).count()

    if recent_postings_quantity_count == None:
        return 0

    # return percentage calculation
    return recent_reservations_count / recent_postings_quantity_count

def avePerResCat(seller_id, category_id):
    recent_postings = Bundle_posting.objects.filter(seller_id=seller_id)
    recent_postings = recent_postings.filter(
        category_id=category_id,
        creation_time__lte=timezone.now() - timedelta(weeks=3)
    )
    recent_postings = recent_postings.filter(
        category_id=category_id,
        creation_time__gte=timezone.now() - timedelta(weeks=6)
    )
    recent_postings_quantity_count = recent_postings.aggregate(Sum("quantity"))[
        "quantity__sum"
    ]
    recent_reservations_count = Reservation.objects.filter(bundle_posting_id__in=recent_postings)
    recent_reservations_count = recent_reservations_count.filter(
        time_stamp__lte=timezone.now() - timedelta(weeks=3),
        time_stamp__gte=timezone.now() - timedelta(weeks=6)
    ).count()
    
    if recent_postings_quantity_count == None:
        return 0

    # return percentage calculation
    return recent_reservations_count / recent_postings_quantity_count



""" Fetch the Sellers Bundle Reservations from between 3 and 6 weeks ago
    and calculate average percentage number of no-shows. """


def avePerNoshow(seller_id):
    recent_reservations = Reservation.objects.filter(posting__seller_id=seller_id)
    recent_reservations = recent_reservations.filter(
        time_stamp__lte=timezone.now() - timedelta(weeks=3)
    )
    recent_reservations = recent_reservations.filter(
        time_stamp__gte=timezone.now() - timedelta(weeks=6)
    )
    recent_reservations_count = recent_reservations.count()

    no_shows = 0
    for reservation in recent_reservations.all():
        if reservation.status == "N":
            no_shows += 1

    if recent_reservations_count == 0:
        return 0

    return no_shows / recent_reservations_count


def errorMSEReservations(seller_id):
    recent_postings = Bundle_posting.objects.filter(seller_id=seller_id)
    recent_postings = recent_postings.filter(
        creation_time__lte=timezone.now() - timedelta(days=1)
    )
    recent_postings = list(
        recent_postings.filter(
            creation_time__gte=timezone.now() - timedelta(weeks=3)
        ).all()
    )

    if len(recent_postings) == 0:
        return 0

    average = avePerRes(seller_id)
    Y_true = [posting.quantity - posting.available for posting in recent_postings]
    Y_pred = [posting.quantity * average for posting in recent_postings]

    return mean_squared_error(Y_true, Y_pred)

def errorMSEReservationsWeekDay(seller_id, day):
    recent_postings = Bundle_posting.objects.filter(seller_id=seller_id)
    recent_postings = recent_postings.filter(
        creation_time__date__day=day
    )
    recent_postings = list(
        recent_postings.filter(
            creation_time__gte=timezone.now() - timedelta(weeks=3),
            creation_time__date__day=day
        ).all()
    )

    if len(recent_postings) == 0:
        return 0

    average = avePerRes(seller_id)
    Y_true = [posting.quantity - posting.available for posting in recent_postings]
    Y_pred = [posting.quantity * average for posting in recent_postings]

    return mean_squared_error(Y_true, Y_pred)


def errorMSENoShow(seller_id):
    recent_postings = Bundle_posting.objects.filter(seller_id=seller_id)
    recent_postings = recent_postings.filter(
        creation_time__lte=timezone.now() - timedelta(days=1)
    )
    recent_postings = list(
        recent_postings.filter(
            creation_time__gte=timezone.now() - timedelta(weeks=3)
        ).all()
    )

    average_n_reservations = avePerRes(seller_id)
    average_no_show = avePerNoshow(seller_id)

    if len(recent_postings) == 0:
        return 0

    Y_true = [
        posting.reservation_set.count()
        - posting.reservation_set.filter(is_collected=True).count()
        for posting in recent_postings
    ]
    Y_pred = [
        posting.quantity * average_n_reservations * average_no_show
        for posting in recent_postings
    ]

    return mean_squared_error(Y_true, Y_pred)
