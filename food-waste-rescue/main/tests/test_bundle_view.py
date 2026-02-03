from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Seller, Bundle

User = get_user_model()

class TestBundleView(TestCase):
    def setUp(self):
        # Create seller user
        self.user = User.objects.create_user(
            username="seller1",
            email="seller@example.com",
            password="pass123",
            user_type="seller",
            display_name="Test Seller"
        )

        # Create seller profile
        self.seller = Seller.objects.create(
            user=self.user,
            location="Test Location",
            opening_time="09:00",
            closing_time="17:00",
            telephone_number="0123456789",
            website_url="https://example.com"
        )
