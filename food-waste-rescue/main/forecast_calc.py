# Contains for forecast
from .models import Bundle_posting, Seller, Reservation
from django.db.models import Sum, Count, F
from django.db import models
from django.utils import timezone
from datetime import time, datetime, timedelta


""" Fetch the Sellers Bundle Reservation from the last 4 weeks
    and calculate average percentage number of reservations."""
def avePerRes(seller_id ):
    recent_postings = Bundle_posting.objects.filter(seller_id=seller_id)
    recent_postings = recent_postings.filter(creation_time__gte=timezone.now() - timedelta(weeks=4))
    recent_postings_quantity_count = recent_postings.aggregate(Sum("quantity"))["quantity__sum"]

    recent_reservations_count = Reservation.objects.filter(posting__seller_id=seller_id).count()

    # return percentage calculation
    return (recent_reservations_count/recent_postings_quantity_count)

""" Fetch the Sellers Bundle Reservations from the last 4 weeks
    and calculate average percentage number of no-shows. """
def avePerNoshow(seller_id):
    recent_reservations = Reservation.objects.filter(posting__seller_id=seller_id)
    recent_reservations = recent_reservations.filter(time_stamp__gte=timezone.now() - timedelta(weeks=4))
    recent_reservations_count = recent_reservations.count()

    no_shows = 0;
    for reservation in recent_reservations.all():
        if reservation.status == "N":
            no_shows += 1

    return (no_shows/recent_reservations_count)
