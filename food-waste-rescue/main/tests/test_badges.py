from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from main.models import (
    Bundle_posting,
    Bundle_posting_category,
    Consumer,
    Reservation,
    Seller,
)
from main.badges import get_badges

User = get_user_model()

class TestBadges(TestCase):

    def setUp(self):
        # create "Consumer" user
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="pass123",
            user_type="consumer",
        )
        # create Consumer profile
        self.consumer = Consumer.objects.create(user=self.user)

        # Create categories
        self.categories = [
            "Meals",
            "Bread & Pastries",
            "Groceries",
            "Flowers & Plants",
            "Pet Food",
            "Vegetarian",
            "Vegan"
        ]
        for category in self.categories:
            Bundle_posting_category.objects.create(name=category)
        
        # create "Seller" user
        self.seller_user = User.objects.create_user(
            username="seller",
            email="seller@example.com",
            password="pass123",
            user_type="seller",
        )

        # create Seller profile

        self.seller = Seller.objects.create(
            user=self.seller_user,
            location="Test Location",
            opening_time="09:00",
            closing_time="18:00",
            telephone_number="0123456789",
            website_url="https://example.com",
            wheelchair=True,
        )

    # Bundle count badges

    def test_badge_one_bundle(self):    
        posting = Bundle_posting.objects.create(
            seller=self.seller,
            category = Bundle_posting_category.objects.get(name="Meals"),
            name="Meal",
            quantity=1,
        )
        Reservation.objects.create(
            posting=posting,
            consumer=self.consumer,
            is_collected=True,
        )

        badges = get_badges(self.consumer)
        badge_names = [badge["name"] for badge in badges]
        self.assertIn("1 Bundle", badge_names)
    
    def test_badge_five_bundles(self):
        category = Bundle_posting_category.objects.get(name="Meals")

        for _ in range(5):
            posting = Bundle_posting.objects.create(
                seller=self.seller,
                category=category,
                name="Meal",
                quantity=1,
            )
            Reservation.objects.create(
                posting=posting,
                consumer=self.consumer,
                is_collected=True,
            )

        badges = get_badges(self.consumer)
        badge_names = [b["name"] for b in badges]

        self.assertIn("5 Bundles", badge_names)

    def test_badge_ten_bundles(self):
        category = Bundle_posting_category.objects.get(name="Meals")

        for _ in range(10):
            posting = Bundle_posting.objects.create(
                seller=self.seller,
                category=category,
                name="Meal",
                quantity=1,
            )
            Reservation.objects.create(
                posting=posting,
                consumer=self.consumer,
                is_collected=True,
            )

        badges = get_badges(self.consumer)
        badge_names = [b["name"] for b in badges]

        self.assertIn("10 Bundles", badge_names)

    def test_badge_twenty_bundles(self):
        category = Bundle_posting_category.objects.get(name="Meals")

        for _ in range(20):
            posting = Bundle_posting.objects.create(
                seller=self.seller,
                category=category,
                name="Meal",
                quantity=1,
            )
            Reservation.objects.create(
                posting=posting,
                consumer=self.consumer,
                is_collected=True,
            )

        badges = get_badges(self.consumer)
        badge_names = [b["name"] for b in badges]

        self.assertIn("20 Bundles", badge_names)

    # category-specific badges

    def test_animal_lover_badge(self):
        pet_cat = Bundle_posting_category.objects.get(name="Pet Food")

        for _ in range(3):
            posting = Bundle_posting.objects.create(
                seller=self.seller,
                category=pet_cat,
                name="Pet Food Bundle",
                quantity=1,
            )
            Reservation.objects.create(
                posting=posting,
                consumer=self.consumer,
                is_collected=True,
            )

        badges = get_badges(self.consumer)
        badge_names = [b["name"] for b in badges]

        self.assertIn("Animal Lover", badge_names)

    def test_very_veggie_badge(self):
        veg_cat = Bundle_posting_category.objects.get(name="Vegetarian")

        for _ in range(3):
            posting = Bundle_posting.objects.create(
                seller=self.seller,
                category=veg_cat,
                name="Veggie Bundle",
                quantity=1,
            )
            Reservation.objects.create(
                posting=posting,
                consumer=self.consumer,
                is_collected=True,
            )

        badges = get_badges(self.consumer)
        badge_names = [b["name"] for b in badges]

        self.assertIn("Very Veggie", badge_names)

    # brian badge (all categories)

    def test_brian_badge(self):
        for cat_name in self.categories:
            cat = Bundle_posting_category.objects.get(name=cat_name)
            posting = Bundle_posting.objects.create(
                seller=self.seller,
                category=cat,
                name="Bundle",
                quantity=1,
            )
            Reservation.objects.create(
                posting=posting,
                consumer=self.consumer,
                is_collected=True,
            )

        badges = get_badges(self.consumer)
        badge_names = [b["name"] for b in badges]

        self.assertIn("Brian Badge", badge_names)
    
    # streak badge tests

    def test_streak_one_week(self):
        """User earns the 1 Week Streak badge after 1 consecutive week with at least one collection."""
        category = Bundle_posting_category.objects.get(name="Meals")

        # 1 collection in each of the last 1 week (i.e., this week)
        for i in range(1):
            posting = Bundle_posting.objects.create(
                seller=self.seller,
                category=category,
                name="Meal",
                quantity=1,
            )
            Reservation.objects.create(
                posting=posting,
                consumer=self.consumer,
                is_collected=True,
                time_stamp=timezone.now() - timedelta(weeks=i),
            )

        badges = get_badges(self.consumer)
        badge_names = [b["name"] for b in badges]

        self.assertIn("1 Week Streak", badge_names)


    def test_streak_one_month(self):
        """User earns the 1 Month Streak badge after 4 consecutive weeks with at least one collection each week."""
        category = Bundle_posting_category.objects.get(name="Meals")

        for i in range(4):  # 4 weeks
            posting = Bundle_posting.objects.create(
                seller=self.seller,
                category=category,
                name="Meal",
                quantity=1,
            )
            Reservation.objects.create(
                posting=posting,
                consumer=self.consumer,
                is_collected=True,
                time_stamp=timezone.now() - timedelta(weeks=i),
            )

        badges = get_badges(self.consumer)
        badge_names = [b["name"] for b in badges]

        self.assertIn("1 Month Streak", badge_names)

    def test_streak_six_months(self):
        """User earns the 6 Month Streak badge after 26 consecutive weeks with at least one collection each week."""
        category = Bundle_posting_category.objects.get(name="Meals")

        for i in range(26):  # ~6 months
            posting = Bundle_posting.objects.create(
                seller=self.seller,
                category=category,
                name="Meal",
                quantity=1,
            )
            Reservation.objects.create(
                posting=posting,
                consumer=self.consumer,
                is_collected=True,
                time_stamp=timezone.now() - timedelta(weeks=i),
            )

        badges = get_badges(self.consumer)
        badge_names = [b["name"] for b in badges]

        self.assertIn("6 Month Streak", badge_names)

    def test_streak_one_year(self):
        """User earns the 1 Year Streak badge after 52 consecutive weeks with at least one collection each week."""
        category = Bundle_posting_category.objects.get(name="Meals")

        for i in range(52):  # 52 weeks
            posting = Bundle_posting.objects.create(
                seller=self.seller,
                category=category,
                name="Meal",
                quantity=1,
            )
            Reservation.objects.create(
                posting=posting,
                consumer=self.consumer,
                is_collected=True,
                time_stamp=timezone.now() - timedelta(weeks=i),
            )

        badges = get_badges(self.consumer)
        badge_names = [b["name"] for b in badges]

        self.assertIn("1 Year Streak", badge_names)
    
    def test_progress_values_for_category_badges(self):
        """Ensure x/y progress values are correct for category-specific badges."""
        pet_cat = Bundle_posting_category.objects.get(name="Pet Food")
        veg_cat = Bundle_posting_category.objects.get(name="Vegetarian")

        # 2 pet food bundles
        for _ in range(2):
            posting = Bundle_posting.objects.create(
                seller=self.seller,
                category=pet_cat,
                name="Pet Food Bundle",
                quantity=1,
            )
            Reservation.objects.create(
                posting=posting,
                consumer=self.consumer,
                is_collected=True,
            )

        # 1 veggie bundle
        posting = Bundle_posting.objects.create(
            seller=self.seller,
            category=veg_cat,
            name="Veggie Bundle",
            quantity=1,
        )
        Reservation.objects.create(
            posting=posting,
            consumer=self.consumer,
            is_collected=True,
        )

        badges = get_badges(self.consumer)
        badge_map = {b["name"]: b for b in badges}

        # Animal Lover (needs 3)
        self.assertEqual(badge_map["Animal Lover"]["x"], 2)
        self.assertEqual(badge_map["Animal Lover"]["y"], 3)

        # Very Veggie (needs 3)
        self.assertEqual(badge_map["Very Veggie"]["x"], 1)
        self.assertEqual(badge_map["Very Veggie"]["y"], 3)

















