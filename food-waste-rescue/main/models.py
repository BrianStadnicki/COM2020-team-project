from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.utils import timezone
from decimal import Decimal

class User(AbstractUser):
    USER_TYPES = (
        ("consumer", "Consumer"),
        ("seller", "Seller")
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES)

class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, default="Exeter University")
    opening_time = models.TimeField(default=datetime.time(9,00))
    closing_time = models.TimeField(default=datetime.time(17,00))
    telephone_number = models.CharField(max_length=100, default="0000000000")
    website_url = models.URLField(default="https://www.test.com")

class Bundle_posting(models.Model):
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)
    category = models.CharField(max_length=100,default="Food")
    name = models.CharField(max_length=100, default="Meat bag")
    contents_description = models.CharField(max_length=500,default="Chicken breast")
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0.00'))
    creation_time = models.DateTimeField(default=timezone.now,blank=True)
    pickup_window_start = models.TimeField(default=datetime.time(18,00))
    pickup_window_end = models.TimeField(default=datetime.time(19,00))
    allergen_celery = models.BooleanField(default=False)
    allergen_crustacean = models.BooleanField(default=False)
    allergen_dairy = models.BooleanField(default=False)
    allergen_egg = models.BooleanField(default=False)
    allergen_fish = models.BooleanField(default=False)
    allergen_gluten = models.BooleanField(default=False)
    allergen_lupin = models.BooleanField(default=False)
    allergen_mollusc = models.BooleanField(default=False)
    allergen_mustard = models.BooleanField(default=False)
    allergen_nut = models.BooleanField(default=False)
    allergen_peanut = models.BooleanField(default=False)
    allergen_sesame = models.BooleanField(default=False)
    allergen_soya = models.BooleanField(default=False)
    allergen_sulphite = models.BooleanField(default=False)

class Reservation(models.Model):
    posting = models.ForeignKey(Bundle_posting,on_delete=models.CASCADE)
    consumer = models.ForeignKey(Consumer,on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(default=timezone.now,blank=True)
    claim_code = models.IntegerField(default=0)
    STATUSES = (
        ("C", "Collected"),
        ("N", "No Show" ),
        ("R", "Reserved"),
        ("E", "Expired")
    )
    status = models.CharField(max_length=1,choices=STATUSES,default="R")
    
class IssueReport(models.Model):
    posting = models.ForeignKey(Bundle_posting,on_delete=models.CASCADE)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    TYPES = (
        ("C","Collection"),
        ("A","Additional information"),
        ("S","Seller")
    )
    type = models.CharField(max_length=1,choices=TYPES,default="C")
    description = models.CharField(max_length=1000,blank=True)
    STATUSES = (
        ("P","Pending"),
        ("A", "Acknowledged"),
        ("R", "Resolved")
    )
    status = models.CharField(max_length=1,choices=STATUSES,default="P")
    creation_time = models.DateTimeField(default=timezone.now,blank=True)
    seller_response = models.CharField(max_length=500,default="Hello consumer!")

class Forecast_output(models.Model):
    posting = models.ForeignKey(Bundle_posting, on_delete=models.CASCADE)
    predicted_reservations = models.IntegerField(default=0)
    predicted_no_show_prob = models.IntegerField(default=0)
    confidence = models.IntegerField(default=0)
    rationale = models.CharField(max_length=1000,blank=True)
    time_recommendation = models.TimeField(blank=True)
    type = models.CharField(max_length=100,default="Linear Regression")
