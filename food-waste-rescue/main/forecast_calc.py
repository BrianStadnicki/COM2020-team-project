# Contains for forecast
from .models import Bundle_posting, Seller, Reservation
from django.db.models import Q
from django.db import models
from django.utils import timezone
import datetime

""" Fetch the Sellers Bundle Reservation from the last 4 weeks
    and calculate average percentage number of reservations."""
def avePerRes( Sid ):
    date = models.DateTimeField(default=timezone.now,blank=True)
    seller = Seller.objects.get(id=Sid)
    # Epoch number for 4 weeks earlier
    four_weeks = 2419200
    # Find bundles and reservations in time frame
    bundles = seller.bundle_postings_set.all().filter(creation_time = date - four_weeks)
    reserved = seller.reservation_set.all().filter(creation_time = date - four_weeks)
    num_of_bundles = len(bundles)
    num_of_reservations = len(reserved)

    # return percentage calculation
    return (num_of_reservations/num_of_bundles)*100

""" Fetch the Sellers Bundle Reservations from the last 4 weeks
    and calculate average percentage number of no-shows. """
def avePerNoshow(Sid):

    date = models.DateTimeField(default=timezone.now,blank=True)
    seller = Seller.objects.get(id=Sid)
    four_weeks = 2419200
    reservations = seller.reservation_set.all().filter(creation_time = date - four_weeks)
    no_shows = seller.reservation_set.all().filter(creation_time = date - four_weeks).filter(status = "N")
    num_of_reservations = len(reservations)
    num_of_no_shows = len(no_shows)

    return (num_of_no_shows/num_of_reservations)*100