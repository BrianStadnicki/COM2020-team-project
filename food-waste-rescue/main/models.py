from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPES = (
        ("consumer", "Consumer"),
        ("seller", "Seller")
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES)

class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    diplay_name = models.CharField(max_length=100, default = "consumer")

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100, default = "seller")
    location = models.CharField(max_length=100, default="Exeter University")
    opening_time = models.TimeField(default="09:00")
    closing_time = models.TimeField(default="17:00")
    telephone_number = models.CharField(max_length=100, default="0000000000")
    website_url = models.URLField(default="https://www.test.com")

class Bundle_posting(models.Model):
    pass


class Reservation(models.Model):
    pass

class IssueReport(models.Model):
    pass
class Forecast_output(models.Model):
    pass


