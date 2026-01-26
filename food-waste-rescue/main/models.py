from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPES = (
        ("consumer", "Consumer"),
        ("seller", "Seller")
    )

class Consumer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    display_name = models.CharField(max_length=100)
