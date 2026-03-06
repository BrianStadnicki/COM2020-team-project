from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Bundle_posting, Consumer, Seller
from django.utils import timezone
from datetime import datetime, time

User = get_user_model()

class TestBundlesView(TestCase):
    def setUp(self):
        # Create consumer user + profile
        self.consumer_user = User.objects.create_user(
            username="consumer1",
            email="consumer@example.com",
            password="consumerpass",
            user_type="consumer",
        )
        
        self.consumer_profile = Consumer.objects.create(
            user=self.consumer_user
        )

        # Create seller user + profile
        self.seller_user = User.objects.create_user(
            username="seller1",
            email="seller@example.com",
            password="pass123",
            user_type="seller",
        )
        
        self.seller = Seller.objects.create(
            user=self.seller_user,
            location="Test Location",
            opening_time="09:00",
            closing_time="18:00",
            telephone_number="0123456789",
            website_url="https://example.com"
        )

        # Create bundles
        self.bundle_posting1 = Bundle_posting.objects.create(
            seller=self.seller,
            category="B&P",
            name="Test Bundle",
            contents_description="Bread",
            quantity=5,
            price=2.00,
            creation_time=timezone.make_aware(datetime(2026, 1, 1, 12, 0)),
            pickup_window_start=time(17, 0),
            pickup_window_end=time(18, 0),
            allergen_gluten=True,
        )

        self.bundle_posting2 = Bundle_posting.objects.create(
            seller=self.seller,
            category="M",
            name="Test Bundle 2",
            contents_description="Peanut Sauce Chicken Curry with Rice",
            quantity=5,
            price=2.00,
            creation_time=timezone.make_aware(datetime(2026, 1, 1, 12, 0)),
            pickup_window_start=time(17, 0),
            pickup_window_end=time(18, 0),
            allergen_dairy=True,
            allergen_nut=True,
            allergen_peanut=True,
        )

        self.bundle_posting3 = Bundle_posting.objects.create(
            seller=self.seller,
            category="G",
            name="Test Bundle 3",
            contents_description="Fruit and Veg Bundle",
            quantity=5,
            price=2.00,
            creation_time=timezone.make_aware(datetime(2026, 1, 1, 12, 0)),
            pickup_window_start=time(17, 0),
            pickup_window_end=time(18, 0),
            # no allergens
        )

    # currently failing
    # but, currently, bundles_view has no logic to filter out expired bundles
    def test_consumer_sees_only_active_bundles(self):
        self.client.login(username="consumer1", password="consumerpass")
        response = self.client.get(reverse("bundles_view_url"))

        posts = response.context["posts"]

        # expired bundle should NOT be included
        self.assertNotIn(self.status == "E", posts)

        # active bundles should be included
        self.assertIn(self.bundle_posting1, posts)
        self.assertIn(self.bundle_posting2, posts)



