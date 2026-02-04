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
            seller = self.seller, 
            category = "Bakery",
            name = "Test bundle",
            contents_description = "Bread"
            quantity = 5
            price = 2.00
            creation_time = timezone.make_aware(datetime(2026, 1, 1, 12, 0))
            pickup_window_start=time(17, 00),
            pickup_window_end=time(18, 00),
            allergen_celery = False,
            allergen_crustacean = False,
            allergen_dairy = False,
            allergen_egg = False,
            allergen_fish = False,
            allergen_gluten = True
            allergen_lupin = False
            allergen_mollusc = False
            allergen_mustard = False
            allergen_nut = False
            allergen_peanut = False
            allergen_sesame = models.BooleanField(default=False)
            allergen_soya = models.BooleanField(default=False)
            allergen_sulphite = models.BooleanField(default=False)
        )

