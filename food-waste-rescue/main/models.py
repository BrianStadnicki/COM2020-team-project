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

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100)
