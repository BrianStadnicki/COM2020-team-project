from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Bundle_posting, Seller
from django.utils import timezone
from datetime import datetime, time

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
            closing_time="18:00",
            telephone_number="0123456789",
            website_url="https://example.com"
        )

        # Create Bundle_posting
        self.bundle_posting = Bundle_posting.objects.create(
            seller = self.seller, 
            category = "Bakery",
            name = "Test Bundle",
            contents_description = "Bread",
            quantity = 5,
            price = 2.00,
            creation_time = timezone.make_aware(datetime(2026, 1, 1, 12, 0)),
            pickup_window_start=time(17, 0),
            pickup_window_end=time(18, 0),
            allergen_celery = False,
            allergen_crustacean = False,
            allergen_dairy = False,
            allergen_egg = False,
            allergen_fish = False,
            allergen_gluten = True,
            allergen_lupin = False,
            allergen_mollusc = False,
            allergen_mustard = False,
            allergen_nut = False,
            allergen_peanut = False,
            allergen_sesame = False,
            allergen_soya = False,
            allergen_sulphite = False
        )

    def test_bundle_view_renders_correct_template(self):
        self.client.login(username="seller1", password="pass123")
        url = reverse("bundle_view_url", args=[self.bundle_posting.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/bundle.html")

        # Checking that the Bundle_posting is associated with the correct seller

        # Checking database relationship directly:
        self.assertEqual(self.bundle_posting.seller, self.seller)

        #Check the view context contains the correct seller:
        response = self.client.get(url)
        self.assertEqual(response.context["post"].seller, self.seller)

        # Content checks

        self.assertContains(response, "Bakery") #testing for correct category
        self.assertContains(response, "Test Bundle") #testing for correct name
        self.assertContains(response, "Bread") #testing for correct contents_description
        self.assertContains(response, "5") #testing for correct quantity
        self.assertContains(response, "£2.00") #testing for correct price

        # Content checks for allergens
        self.assertNotContains(response, "Celery")
        self.assertNotContains(response, "Crustacean")
        self.assertNotContains(response, "Dairy")
        self.assertNotContains(response, "Egg")
        self.assertNotContains(response, "Fish")
        self.assertContains(response, "Gluten")
        self.assertNotContains(response, "Lupin")
        self.assertNotContains(response, "Mollusc")
        self.assertNotContains(response, "Mustanrd")
        self.assertNotContains(response, "Nut")
        self.assertNotContains(response, "Peanut")
        self.assertNotContains(response, "Sesame")
        self.assertNotContains(response, "Soya")
        self.assertNotContains(response, "Sulphite")

        # Content checks for Seller info

        self.assertContains(response, "seller1")
        self.assertContains(response, "Test Location")
        self.assertContains(response, "9:00")
        self.assertContains(response, "18:00")
        self.assertContains(response, "0123456789")
        self.assertContains(response, "https://example.com")

        # Content checks for pickup window
        self.assertContains(response, "17:00")
        self.assertContains(response, "18:00")
        

        