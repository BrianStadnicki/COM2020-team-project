from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Bundle_posting, Seller

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

        # Create Bundle_posting
        self.bundle_posting = Bundle_posting.objects.create(
            seller = self.seller #only field without a default
            #the other fields will have defaults, but can be set values for testing purposes - determine if this is necessary
        )

        #CONTINUE HERE