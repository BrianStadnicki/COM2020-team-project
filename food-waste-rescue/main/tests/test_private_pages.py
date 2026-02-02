from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model

User = get_user_model()

"""
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

Public / both Seller and Consumer pages
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