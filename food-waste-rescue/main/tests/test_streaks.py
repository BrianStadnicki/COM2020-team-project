from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from main.models import Consumer, Seller, Bundle_posting, Bundle_posting_category, Reservation
from main.badges import get_longest_streak

User = get_user_model()

class TestWeeklyStreakLogic(TestCase):

    def setUp(self):
        # Hard reset: ensure no leftover reservations from other tests
        Reservation.objects.all().delete()

        self.user = User.objects.create_user(
            username="streak_user",
            email="streak@example.com",
            password="pass123",
            user_type="consumer",
        )
        self.consumer = Consumer.objects.create(user=self.user)


        # Same categories as test_badges
        self.categories = [
            "Meals",
            "Bread & Pastries",
            "Groceries",
            "Flowers & Plants",
            "Pet Food",
            "Vegetarian",
            "Vegan"
        ]
        for cat in self.categories:
            Bundle_posting_category.objects.create(name=cat)

        self.default_category = Bundle_posting_category.objects.get(name="Meals")

        self.seller_user = User.objects.create_user(
            username="seller",
            email="seller@example.com",
            password="pass123",
            user_type="seller",
        )
        self.seller = Seller.objects.create(user=self.seller_user)

    def create_reservation_weeks_ago(self, weeks):
        posting = Bundle_posting.objects.create(
            seller=self.seller,
            category=self.default_category,
            name="Meal",
            quantity=1,
        )
        ts = timezone.now() - timedelta(weeks=weeks)
        return Reservation.objects.create(
            posting=posting,
            consumer=self.consumer,
            is_collected=True,
            time_stamp=ts,
        )

    # Weekly streak tests

    def test_streak_zero(self):
        self.assertEqual(get_longest_streak(self.consumer), 0)

    def test_streak_one_week(self):
        self.create_reservation_weeks_ago(0)
        self.assertEqual(get_longest_streak(self.consumer), 1)

    def test_streak_three_weeks(self):
        self.create_reservation_weeks_ago(0)
        self.create_reservation_weeks_ago(1)
        self.create_reservation_weeks_ago(2)
        self.assertEqual(get_longest_streak(self.consumer), 3)

    def test_streak_break(self):
        self.create_reservation_weeks_ago(0)
        self.create_reservation_weeks_ago(1)
        self.create_reservation_weeks_ago(3)
        self.assertEqual(get_longest_streak(self.consumer), 2)

    def test_multiple_reservations_same_week(self):
        self.create_reservation_weeks_ago(0)
        self.create_reservation_weeks_ago(0)
        self.create_reservation_weeks_ago(1)
        self.assertEqual(get_longest_streak(self.consumer), 2)

    def test_non_consecutive_weeks(self):
        self.create_reservation_weeks_ago(0)
        self.create_reservation_weeks_ago(2)
        self.assertEqual(get_longest_streak(self.consumer), 1)

