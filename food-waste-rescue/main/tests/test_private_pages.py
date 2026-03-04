from datetime import time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Bundle_posting, Seller

User = get_user_model()

"""
ACCESS CONTROL RULES

Anonymous (not logged in) users should get 302 Redirect when trying to access
pages that require logging in (every page with the exception of login, signup, 
and seller-extra).

Logged in users should get 200 OK as long as the page corresponds to their 
role type (e.g. Consumers should see Consumer pages but not pages restricted to 
just Sellers.)

Logged-in wrong-role users should get 403 Forbidden.

Seller-only pages:
bundle_new_view
bundle_confirm_view
analytics_view

For anonymous users, redirect to login.
For Consumers, 403 Forbidden.
For Sellers, 200 OK.

Both Seller and Consumer pages - still require login!
bundles_view
bundle_view
reports_view
report_view(id)
report_new_view
impact_view
accessibility_view
reservations_view
reservation_view(id)

For anonymous users, redirect to login.
For Consumers, 200 OK.
For Sellers, 200 OK.

"""

# ----------------------------------------------------------------------------------
# SELLER ONLY PAGES

class TestSellerOnlyPages(TestCase):
    """
    This will test that Seller-only pages will return 200 OK for Sellers,
    redirect to login for anonymous users, and return 403 Forbidden for Consumers.

    The Seller-only pages are bundle_new_view, bundle_confirm_view, and analytics_view.
    """
    def setUp(self):
        # Create a mock Consumer
        self.consumer = User.objects.create_user(
            username="consumer1",
            email="mockconsumer@gmail.com",
            password="consumerpass1",
            user_type="consumer"
        )
        # Create a mock Seller
        self.seller = User.objects.create_user(
            username="seller1",
            email="mockseller@gmail.com",
            password="sellerpass1",
            user_type="seller"
        )
    
    #passes
    def test_seller_extra_page_requires_login(self):
        url = reverse("seller-extra")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)
        self.assertTrue(response.url.startswith("/accounts/login"))

    #passes
    def test_seller_extra_page_accessible_to_logged_in_seller(self):
        seller = User.objects.create_user(
            username="seller_test",
            email="mockuser@gmail.com",
            password="password123",
            user_type="seller",
        )
        self.client.login(username="seller_test", password="password123")
        url = reverse("seller-extra")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/seller_extra.html")
    
    #passes
    def test_seller_extra_blocks_consumer(self):
        """Users should only be able to access 'seller-extra' if they selected 'Seller' in
        the registration page."""
        consumer = User.objects.create_user(
            username="consumer_test",
            email="mockuser2@gmail.com",
            password="password456",
            user_type = "consumer"
        )
        self.client.login(username="consumer_test", password="password456")
        url = reverse("seller-extra")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    # -----------------------------------------------------------------------------
    #Tests for bundle_new_view 

    #passes
    def test_bundle_new_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("bundle_new_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)
        self.assertTrue(response.url.startswith("/accounts/login"))
    
    #passes
    def test_bundle_new_forbidden_for_consumer(self):
        """Consumers should get 403 Forbidden for Seller-only pages"""
        self.client.login(username="consumer1", password="consumerpass1")
        url = reverse("bundle_new_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    #passes
    def test_bundle_new_allows_seller(self):
        """Sellers should get 200 OK for Seller-only pages"""
        self.client.login(username="seller1", password="sellerpass1")
        url = reverse("bundle_new_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    # ----------------------------------------------------------------------------

    #Tests for analytics_view

    #passes
    def test_analytics_view_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("analytics_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)
        self.assertTrue(response.url.startswith("/accounts/login"))

    #passes
    def test_analytics_view_forbidden_for_consumer(self):
        """Consumers should get 403 Forbidden for Seller-only pages"""
        self.client.login(username="consumer1", password="consumerpass1")
        url = reverse("analytics_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
    
    # passes
    def test_analytics_view_allows_seller(self):
        seller = User.objects.create_user(
            username="seller_test2",
            email="mockuser2@gmail.com",
            password="password789",
            user_type="seller",
        )

        # Create the Seller profile so onboarding is complete
        Seller.objects.create(
            user=seller,
        )

        self.client.login(username="seller_test2", password="password789")

        url = reverse("analytics_view_url")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/analytics.html")

    # --------------------------------------------------------------------------------

class testSellerAndConsumerPages(TestCase):

    """
    This will test pages that are private (cannot be accessed by anonymous users),
    however, are available for all logged in users (both Consumers and Sellers).

    For anonymous users, redirect to login.
    For Consumers, 200 OK.
    For Sellers, 200 OK.
    """

    def setUp(self):
        # Create a mock Consumer
        self.consumer_user = User.objects.create_user(
            username="test_consumer2",
            email="mockconsumer2@gmail.com",
            password="consumerpass2",
            user_type="consumer"
        )

        # Create a mock Seller user
        self.seller_user = User.objects.create_user(
            username="test_seller2",
            email="mockseller2@gmail.com",
            password="sellerpass2",
            user_type="seller"
        )

        # Create the Seller profile
        self.seller_profile = Seller.objects.create(
            user=self.seller_user,
            location="Test Location",
            opening_time="09:00",
            closing_time="17:00",
            telephone_number="0123456789",
            website_url="https://example.com"
        )

        # Create a mock bundle
        self.bundle_posting = Bundle_posting.objects.create(
            seller=self.seller_profile,
            category="Bakery",
            name="Test Bundle",
            contents_description="Bread",
            quantity=5,
            price=2.00,
            pickup_window_start=time(14, 0),
            pickup_window_end=time(15, 0),
        )   


    # -----------------------------------------------------------------------------
    #Tests for bundles_view
    
    #passes
    def test_bundles_view_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("bundles_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)
    
    #passes
    def test_bundles_view_allows_consumer(self):
        """Consumers should get 200 OK"""
        self.client.login(username="test_consumer2", password="consumerpass2")
        url = reverse("bundles_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/bundles.html")

    #passes
    def test_bundles_view_allows_seller(self):
        """Sellers should get 200 OK"""
        self.client.login(username="test_seller2", password="sellerpass2")
        url = reverse("bundles_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/bundles.html")
    
    # -----------------------------------------------------------------------------
    #Tests for bundle_view

    #passes
    def test_bundle_view_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("bundle_view_url", args=[self.bundle_posting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        
    #passes
    def test_bundle_view_allows_consumer(self):
        """Consumers should get 200 OK or 302 Redirect"""
        self.client.login(username="consumer2", password="consumerpass2")
        url = reverse("bundle_view_url", args=[self.bundle_posting.id])
        response = self.client.get(url)
        self.assertIn(response.status_code, (200, 302))

    #passes
    def test_bundle_view_allows_owner_seller(self):
        self.client.login(username="test_seller2", password="sellerpass2")
        url = reverse("bundle_view_url", args=[self.bundle_posting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # currently failing: AssertionError: 200 != 302
    def test_bundle_view_redirects_seller_without_profile(self):
    # create a seller user but DO NOT create Seller profile
        user = User.objects.create_user(
            username="seller_no_profile", password="pass", user_type="seller"
        )
        self.client.login(username="seller_no_profile", password="pass")
        url = reverse("bundle_view_url", args=[self.bundle_posting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("seller-extra"), response.url)

    #currently failing: AssertionError: 200 != 403
    def test_bundle_view_non_owner_seller(self):
        other_user = User.objects.create_user(
            username="other_seller", password="pass", user_type="seller"
        )
        other_profile = Seller.objects.create(user=other_user, location="X", opening_time="09:00", closing_time="17:00", telephone_number="0", website_url="https://x")
        self.client.login(username="other_seller", password="pass")
        url = reverse("bundle_view_url", args=[self.bundle_posting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    #-----------------------------------------------------------------------------

    #Tests for reports_view

    #passes
    def test_reports_view_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("reports_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)

    #failing
    def test_reports_view_allows_consumer(self):
        """Consumers should get 200 OK"""
        self.client.login(username="consumer2", password="consumerpass2")
        url = reverse("reports_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/reports.html")

    def test_reports_view_allows_seller(self):
        """Sellers shoud get 200 OK"""
        self.client.login(username="seller2", password="sellerpass2")
        url = reverse("reports_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/reports.html")

    # ---------------------------------------------------------------------------

    #Tests for report_view(id)
    def test_report_view_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("report_view_url", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)
    
    def test_report_view_allows_consumer(self):
        """Consumers should get 200 OK"""
        self.client.login(username="consumer2", password="consumerpass2")
        url = reverse("report_view_url", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_report_view_allows_seller(self):
        """Sellers shoud get 200 OK"""
        self.client.login(username="seller2", password="sellerpass2")
        url = reverse("report_view_url", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # ---------------------------------------------------------------------------

    #Tests for report_new_view

    def test_report_new_view_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("report_new_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)
    
    def test_report_new_view_allows_consumer(self):
        """Consumers should get 200 OK"""
        self.client.login(username="consumer2", password="consumerpass2")
        url = reverse("report_new_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_report_new_view_allows_seller(self):
        """Sellers shoud get 200 OK"""
        self.client.login(username="seller2", password="sellerpass2")
        url = reverse("report_new_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    # ---------------------------------------------------------------------------

    #Tests for impact_view

    def test_impact_view_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("impact_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)
    
    def test_impact_view_allows_consumer(self):
        """Consumers should get 200 OK"""
        self.client.login(username="consumer2", password="consumerpass2")
        url = reverse("impact_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_impact_view_allows_seller(self):
        """Sellers shoud get 200 OK"""
        self.client.login(username="seller2", password="sellerpass2")
        url = reverse("impact_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
    # ---------------------------------------------------------------------------

    #Tests for accessibility_view

    def test_accessibility_view_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("accessibility_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)
    
    def test_accessibility_view_allows_consumer(self):
        """Consumers should get 200 OK"""
        self.client.login(username="consumer2", password="consumerpass2")
        url = reverse("accessibility_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_accessibility_view_allows_seller(self):
        """Sellers shoud get 200 OK"""
        self.client.login(username="seller2", password="sellerpass2")
        url = reverse("accessibility_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # ---------------------------------------------------------------------------

    #Tests for reservations_view

    def test_reservations_view_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("reservations_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)
    
    def test_reservations_view_allows_consumer(self):
        """Consumers should get 200 OK"""
        self.client.login(username="consumer2", password="consumerpass2")
        url = reverse("reservations_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_reservations_view_allows_seller(self):
        """Sellers shoud get 200 OK"""
        self.client.login(username="seller2", password="sellerpass2")
        url = reverse("reservations_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    # -----------------------------------------------------------------------------

    #Tests for reservation_view(id)

    def test_reservation_view_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("reservation_view_url", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)
    
    def test_reservation_view_allows_consumer(self):
        """Consumers should get 200 OK"""
        self.client.login(username="consumer2", password="consumerpass2")
        url = reverse("reservation_view_url", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_reservation_view_allows_seller(self):
        """Sellers shoud get 200 OK"""
        self.client.login(username="seller2", password="sellerpass2")
        url = reverse("reservation_view_url", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
