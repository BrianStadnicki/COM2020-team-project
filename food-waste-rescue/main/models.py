from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPES = (
        ("consumer", "Consumer"),
        ("seller", "Seller")
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPES, default="consumer")

class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    diplay_name = models.CharField(max_length=100)

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    telephone_number = models.CharField(max_length=100)
    website_url = models.URLField()

class Bundle_posting(models.Model):
    pass


class Reservation(models.Model):
    pass

class IssueReport(models.Model):
    pass
class Forecast_output(models.Model):
    pass


