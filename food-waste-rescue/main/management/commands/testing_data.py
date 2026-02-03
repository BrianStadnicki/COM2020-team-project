import datetime
from decimal import Decimal
from typing import Any
from django.core.management.base import BaseCommand, CommandError, CommandParser
from main.models import User, Seller, Bundle_posting, IssueReport, Consumer

class Command(BaseCommand):
    help = "Create some simple testing data"

    def handle(self, *args: Any, **options: Any) -> str | None:
        users_consumer = [User.objects.create_user(f"consumer{i}", f"cons{i}@test.com", "password", user_type="consumer") for i in range(5)]
        consumers = [Consumer.objects.create(user=users_consumer[i]) for i in range(5)]
        users_seller = [User.objects.create_user(f"seller{i}", f"sell{i}@test.com", "password", user_type="seller") for i in range(3)]
        seller_profiles = [Seller.objects.create(user=users_seller[i], location=f"exeter{i}", opening_time=datetime.time(i + 8,00), closing_time=datetime.time(i + 20,00), telephone_number=f"234234{i}", website_url=f"https://seller{i}.com") for i in range(3)]
        bundle_postings = [Bundle_posting.objects.create(seller=seller_profiles[i%3], category=["Food","Drugs"][i%2], name=f"Meat bag {i}", contents_description=f"It contains {i} snails", quantity=i+5, price=Decimal(i), pickup_window_start=datetime.time(12+i,00), pickup_window_end=datetime.time(14+i,00), allergen_celery=(i%2==0), allergen_egg=(i%3==0), allergen_soya=((i+1)%3==0)) for i in range(9)]
        reservations = [IssueReport.objects.create(posting=bundle_postings[i%7], consumer=consumers[i%4]) for i in range(20)]
    