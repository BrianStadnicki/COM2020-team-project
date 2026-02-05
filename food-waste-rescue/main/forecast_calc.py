# Contains for forecast
from .models import Bundle_posting, Seller, Reservation
from django.db.models import Q
from django.db import models
from django.utils import timezone
import datetime

""" Fetch the Sellers Bundle Reservation from the last 4 weeks
    and calculate average percentage number of reservations."""
def avePerRes( Sid ):
    # Get current date
    # Get all bundles from last 4 weeks
    # Get bundle quantity
    # Get number of reservations
    # Find percentage, return it
    seller = Seller.objects.get(id=Sid)
    bundles = seller.bundle_postings_set.all()

    date = models.DateTimeField(default=timezone.now,blank=True) # is this epoch in milliseconds or datetime.datetime object
    lastMonthBundles = []
    for bundle in bundles:
        if bundle.creation_time > 
    pass

""" Fetch the Sellers Bundle Reservations from the last 4 weeks
    and calculate average percentage number of no-shows. """
def avePerNoshow():
    # Get current date
    # Get all reservations from past 4 weeks
    # Calc percent of no-shows from reservations
    pass