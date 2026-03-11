from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Bundle_posting, Bundle_posting_category, Consumer, Reservation, Seller
from django.utils import timezone
from datetime import datetime, time, timedelta
from django.db.models import Count, Q, F

User = get_user_model()

class TestBundlesView(TestCase):
    def setUp(self):
        CATEGORIES = [
            "Meals",
            "Bread & Pastries",
            "Groceries",
            "Flowers & Plants",
            "Pet Food",
            "Vegetarian",
            "Vegan"
        ]
        for category in CATEGORIES:
            Bundle_posting_category.objects.create(name=category)

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
            website_url="https://example.com",
            wheelchair=True,
        )

        # Create bundles

        # Active bundle
        self.bundle_posting1 = Bundle_posting.objects.create(
            seller=self.seller,
            category = Bundle_posting_category.objects.get(name="Bread & Pastries"),
            name="Test Bundle",
            contents_description="Bread",
            quantity=5,
            price=2.00,
            creation_time=timezone.now(),
            pickup_window_start=time(0, 0),
            pickup_window_end=time(23, 59),
            allergen_gluten=True,
        )

        # Expired bundle
        self.bundle_posting2 = Bundle_posting.objects.create(
            seller=self.seller,
            category = Bundle_posting_category.objects.get(name="Meals"),
            name="Test Bundle 2",
            contents_description="Peanut Sauce Chicken Curry with Rice",
            quantity=5,
            price=2.00,
            creation_time=timezone.now() - timedelta(days=1),
            pickup_window_start=time(0, 0),
            pickup_window_end=time(0, 0),
            allergen_dairy=True,
            allergen_nut=True,
            allergen_peanut=True,
        )

        # Inactive bundle (fully collected)
        self.bundle_posting3 = Bundle_posting.objects.create(
            seller=self.seller,
            category = Bundle_posting_category.objects.get(name="Groceries"),
            name="Test Bundle 3",
            contents_description="Fruit and Veg Bundle",
            quantity=1,
            price=2.00,
            creation_time=timezone.now(),
            pickup_window_start=time(17, 0),
            pickup_window_end=time(23, 59),
        )
        Reservation.objects.create(
            posting=self.bundle_posting3,
            consumer=self.consumer_profile,
            is_collected=True,
        )

    # Default behaviour 

    # passes
    def test_consumer_sees_only_active_bundles(self):
        self.client.login(username="consumer1", password="consumerpass")
        response = self.client.get(reverse("bundles_view_url"))
        posts = response.context["posts"]

        self.assertIn(self.bundle_posting1, posts)   # active
        self.assertNotIn(self.bundle_posting2, posts)  # expired
        self.assertNotIn(self.bundle_posting3, posts)  # inactive

    def test_seller_sees_only_active_bundles_by_default(self):
        self.client.login(username="seller1", password="pass123")
        response = self.client.get(reverse("bundles_view_url"))
        posts = response.context["posts"]

        # Active bundle should be visible
        self.assertIn(self.bundle_posting1, posts)

        # Expired bundle should NOT be visible by default
        self.assertNotIn(self.bundle_posting2, posts)

        # Inactive bundle should NOT be visible by default
        self.assertNotIn(self.bundle_posting3, posts)

    # filters

    # passes
    def test_filter_show_expired(self):
        self.client.login(username="consumer1", password="consumerpass")
        response = self.client.get(reverse("bundles_view_url") + "?show-expired=1")
        posts = response.context["posts"]
        self.assertIn(self.bundle_posting2, posts)

    def test_filter_show_inactive(self):
        """Inactive bundles appear when ?show-inactive=1 is used."""
        self.client.login(username="seller1", password="pass123")
        response = self.client.get(reverse("bundles_view_url") + "?show-inactive=1")
        posts = response.context["posts"]
        self.assertIn(self.bundle_posting3, posts)

    def test_filter_by_location(self):
        """Location filter should match seller location."""
        self.client.login(username="consumer1", password="consumerpass")
        response = self.client.get(reverse("bundles_view_url") + "?location=Test")
        posts = response.context["posts"]
        self.assertIn(self.bundle_posting1, posts)

    def test_filter_excluded_allergens(self):
        """Bundles containing excluded allergens should be removed."""
        self.client.login(username="consumer1", password="consumerpass")
        response = self.client.get(reverse("bundles_view_url") + "?excluded-allergens=gluten")
        posts = response.context["posts"]
        self.assertNotIn(self.bundle_posting1, posts)  # contains gluten

    def test_filter_wheelchair_accessible(self):
        """Wheelchair filter should show only accessible sellers."""
        self.client.login(username="consumer1", password="consumerpass")
        response = self.client.get(reverse("bundles_view_url") + "?wheelchair=1")
        posts = response.context["posts"]
        self.assertIn(self.bundle_posting1, posts)

    # post actions
    def test_validate_claim_code_success(self):
        reservation = Reservation.objects.create(
            posting=self.bundle_posting1,
            consumer=self.consumer_profile,
        )
        reservation.claim_code_generator()
        self.client.login(username="consumer1", password="consumerpass")
        response = self.client.post(
            reverse("bundles_view_url"),
            {"submit": "validate_code", "claim_code": reservation.claim_code},
        )
        self.assertEqual(response.context["matched_reservation"], reservation)
        self.assertIsNone(response.context["error"])

    def test_validate_claim_code_invalid(self):
        self.client.login(username="consumer1", password="consumerpass")
        response = self.client.post(
            reverse("bundles_view_url"),
            {"submit": "validate_code", "claim_code": "999999"},
        )

        self.assertEqual(response.context["error"], "Invalid claim code")

    def test_seller_marks_reservation_collected(self):
        reservation = Reservation.objects.create(
            posting=self.bundle_posting1,
            consumer=self.consumer_profile,
        )

        self.client.login(username="seller1", password="pass123")
        self.client.post(
            reverse("bundles_view_url"),
            {"submit": "Collected?", "id": reservation.id},
        )

        reservation.refresh_from_db()
        self.assertTrue(reservation.is_collected)





