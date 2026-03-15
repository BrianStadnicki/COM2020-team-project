from django.test import TestCase
from django.contrib.auth import get_user_model
from main.models import Bundle_posting, Bundle_posting_category, Consumer, Reservation, Seller
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

    #passes
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




