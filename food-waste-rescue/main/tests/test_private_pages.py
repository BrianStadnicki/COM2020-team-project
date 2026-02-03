from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

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
reservatuib_view(id)

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

    # -----------------------------------------------------------------------------
    #Tests for bundle_new_view 

    #currently failing: AssertionError: 200 != 302
    def test_bundle_new_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("bundle_new_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)
    
    #currently failing: AssertionError: 200 != 403
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
        self.assertTemplateUsed(response, "main/bundle_new.html")
    
    # ----------------------------------------------------------------------------

    #Tests for bundle_confirm_view

    #currently failing: AssertionError: 200 != 302
    def test_bundle_confirm_view_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("bundle_confirm_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("accounts/login", response.url)

    #currently failing: AssertonError: 200 != 403
    def test_bundle_confirm_view_forbidden_for_consumer(self):
        """Consumers should get 403 Forbidden for Seller-only pages"""
        self.client.login(username="consumer1", password="consumerpass1")
        url = reverse("bundle_confirm_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    #passes
    def test_bundle_confirm_view_allows_seller(self):
        """Sellers should get 200 OK for Seller-only pages"""
        self.client.login(username="seller1",password="sellerpass1")
        url = reverse("bundle_confirm_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/bundle_confirm.html")

    # --------------------------------------------------------------------------------

    #Tests for analytics_view

    def test_analytics_view_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("analytics_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)

    def test_analytics_view_forbidden_for_consumer(self):
        """Anonymous users should get 403 Forbidden for Seller-only pages"""
        self.client.login(username="consumer1", password="consumerpass1")
        url = reverse("analytics_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
    
    def test_analytics_view_allows_seller(self):
        """Sellers should get 200 OK for Seller-only pages"""
        self.client.login(username="seller1", password="sellerpass1")
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
        self.consumer = User.objects.create_user(
            username="consumer2",
            email="mockconsumer2@gmail.com",
            password="consumerpass2",
            user_type="consumer"
        )
        # Create a mock Seller
        self.seller = User.objects.create_user(
            username="seller2",
            email="mockseller2@gmail.com",
            password="sellerpass2",
            user_type="seller"
        )

    # -----------------------------------------------------------------------------
    #Tests for bundles_view

    def test_bundles_view_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("bundles_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)
    
    def test_bundles_view_allows_consumer(self):
        """Consumers should get 200 OK"""
        self.client.login(username="consumer2", password="consumerpass2")
        url = reverse("bundles_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/bundle.html")

    def test_bundles_view_allows_seller(self):
        """Sellers should get 200 OK"""
        self.client.login(username="seller2", password="sellerpass2")
        url = reverse("bundles_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/bundle.html")
    
    # -----------------------------------------------------------------------------
    #Tests for bundle_view

    def test_bundle_view_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("bundle_view_url", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)

    def test_bundle_view_allows_consumer(self):
        """Consumers should get 200 OK"""
        self.client.login(username="consumer2", password="consumerpass2")
        url = reverse("bundle_view_url", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_bundles_view_allows_seller(self):
        """Sellers should get 200 OK"""
        self.client.login(username="seller2", password="sellerpass2")
        url = reverse("bundle_view_url", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    #-----------------------------------------------------------------------------

    #Tests for reports_view

    def test_reports_view_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("reports_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)
    
    def test_reports_view_allows_consumer(self):
        """Consumers should get 200 OK"""
        self.client.login(username="consumer2", password="consumerpass2")
        url = reverse("reports_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_reports_view_allows_seller(self):
        """Sellers shoud get 200 OK"""
        self.client.login(username="seller2", password="sellerpass2")
        url = reverse("reports_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    

