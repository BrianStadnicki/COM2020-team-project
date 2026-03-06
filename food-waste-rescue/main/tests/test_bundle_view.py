from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Bundle_posting, Seller
from django.utils import timezone
from datetime import datetime, time

User = get_user_model()

class TestBundleView(TestCase):
    def setUp(self):
        # Create consumer user
        self.consumer_user = User.objects.create_user(
            username="consumer1",
            email="consumer@example.com",
            password="consumerpass",
            user_type="consumer",
        )

        # Create seller user
        self.user = User.objects.create_user(
            username="seller1",
            email="seller@example.com",
            password="pass123",
            user_type="seller",
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
            category = "B&P",
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

    #passes
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

        self.assertTrue(
            "Bread & Pastries" in response.content.decode()
            or "Bread &amp; Pastries" in response.content.decode()
        ) #testing for correct category
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
        self.assertNotContains(response, "Mustard")
        self.assertNotContains(response, "Nut")
        self.assertNotContains(response, "Peanut")
        self.assertNotContains(response, "Sesame")
        self.assertNotContains(response, "Soya")
        self.assertNotContains(response, "Sulphite")

        # Content checks for Seller info

        self.assertContains(response, "seller1")
        self.assertContains(response, "Test Location")
        self.assertContains(response, "9 a.m.")
        self.assertContains(response, "6 p.m.")
        self.assertContains(response, "0123456789")
        self.assertContains(response, "https://example.com")

        # Content checks for pickup window
        self.assertContains(response, "5 p.m.")
        self.assertContains(response, "6 p.m.")
    
    # passes
    def test_bundle_view_404_for_missing_bundle(self):
        self.client.login(username="seller1", password="pass123")
        url = reverse("bundle_view_url", args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    # AssertionError: 302 != 403
    def test_consumer_cannot_view_expired_bundle(self):
        ''' Consumer cannot view expired bundles'''
        # setting the pickup window to be in the past
        # this means the bundle is expired
        self.bundle_posting.pickup_window_end = time(0, 0)  
        self.bundle_posting.save()

        # logging in as the mock consumer
        self.client.login(username="consumer1", password="consumerpass")
        url = reverse("bundle_view_url", args=[self.bundle_posting.id])
        response = self.client.get(url)

        # the consumer should be forbidden from accessing expired bundles
        self.assertEqual(response.status_code, 403)

    #passes
    def test_seller_can_view_expired_bundle(self):
        '''Seller can still view expired bundles'''
        # setting the pickup window to be in the past
        # this means the bundle is expired
        self.bundle_posting.pickup_window_end = time(0, 0)
        self.bundle_posting.save()

        # logging in as the mock seller
        # this seller should be able to view all the bundles they created including expired bundles
        self.client.login(username="seller1", password="pass123")
        url = reverse("bundle_view_url", args=[self.bundle_posting.id])
        response = self.client.get(url)

        # the seller should be able to see the expired bundle
        self.assertEqual(response.status_code, 200)
    
    # passes
    def test_consumer_cannot_view_deleted_bundle(self):
        '''Consumer cannot view deleted bundles'''
        # deleting the mock bundle
        bundle_id = self.bundle_posting.id
        self.bundle_posting.delete()

        # logging in as the consumer
        self.client.login(username="consumer1", password="consumerpass")
        url = reverse("bundle_view_url", args=[bundle_id])
        response = self.client.get(url)

        # the consumer should be forbidden from viewing the deleted bundle
        self.assertEqual(response.status_code, 404)


        