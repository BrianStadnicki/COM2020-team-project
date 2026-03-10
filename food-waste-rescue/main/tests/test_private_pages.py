from datetime import time
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from main.models import Bundle_posting, Bundle_posting_category, Consumer, IssueReport, Seller

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

Consumer-only pages:
report_new_view

For anonymous users, redirect to login.
For Consumers, 200 OK.
For Sellers, 403 Forbidden.

Both Seller and Consumer pages - still require login!
bundles_view
bundle_view
reports_view
report_view(id)
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

        # Create a mock Consumer
        self.consumer_user = User.objects.create_user(
            username="consumer1",
            email="mockconsumer@gmail.com",
            password="consumerpass1",
            user_type="consumer"
        )

        # Create Consumer profile
        self.consumer_profile = Consumer.objects.create(
            user=self.consumer_user
        )

        # Create a mock Seller
        self.seller_user = User.objects.create_user(
            username="seller1",
            email="mockseller@gmail.com",
            password="sellerpass1",
            user_type="seller"
        )

        # Create Seller Profile
        self.seller_profile = Seller.objects.create(
            user=self.seller_user,
            location="Test Location",
            opening_time="09:00",
            closing_time="18:00",
            telephone_number="0123456789",
            website_url="https://example.com"
        )
    
    #passes
    def test_seller_profile_page_requires_login(self):
        url = reverse("seller_profile_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)

    #passes
    def test_seller_profile_page_accessible_to_new_seller(self):
        new_seller = User.objects.create_user(
            username="new_seller",
            email="new_seller@gmail.com",
            password="newpass",
            user_type="seller"
        )

        logged_in = self.client.login(username="new_seller", password="newpass")
        url = reverse("seller_profile_view_url")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
    
    #passes
    def test_existing_seller_can_edit_profile(self):
        # Log in the existing seller created in setUp()
        logged_in = self.client.login(username="seller1", password="sellerpass1")
        self.assertTrue(logged_in)

        url = reverse("seller_profile_view_url")
        response = self.client.get(url)

        # Should be allowed to access the page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/seller_profile.html")

        # Form should be pre-filled with existing profile data
        form = response.context["form"]

        self.assertEqual(form.initial["location"], "Test Location")
        self.assertEqual(form.initial["opening_time"], "09:00")
        self.assertEqual(form.initial["closing_time"], "18:00")
        self.assertEqual(form.initial["telephone_number"], "0123456789")
        self.assertEqual(form.initial["website_url"], "https://example.com")
    
    #passes
    def test_seller_profile_page_blocks_consumer(self):
        """Users should only be able to access 'seller-extra' if they selected 'Seller' in
        the registration page."""
        consumer = User.objects.create_user(
            username="consumer_test",
            email="mockuser2@gmail.com",
            password="password456",
            user_type = "consumer"
        )
        self.client.login(username="consumer_test", password="password456")
        url = reverse("seller_profile_view_url")
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

        # Create a mock Consumer
        self.consumer_user = User.objects.create_user(
            username="test_consumer2",
            email="mockconsumer2@gmail.com",
            password="consumerpass2",
            user_type="consumer"
        )

        self.consumer_profile = Consumer.objects.create(
            user=self.consumer_user,
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

    # creating a mock IssueReport
    def create_report(self, creator_consumer=None, posting=None, **kwargs):
        return IssueReport.objects.create(
            posting=posting or self.bundle_posting,
            consumer=creator_consumer or self.consumer_profile,
            description=kwargs.get("description", "Test report"),
            type=kwargs.get("type", "C"),
            status=kwargs.get("status", "P"),
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
            username="seller_without_profile",
            email="seller_without_profile@gmail.com",
            password="password1234",
            user_type="seller"
        )
        self.client.login(username="seller_no_profile", password="pass")
        url = reverse("bundle_view_url", args=[self.bundle_posting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response, "registration/seller_profile.html")
        

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

    #passes
    def test_reports_view_allows_consumer_creator(self):
        # Create a report owned by the Consumer
        report = self.create_report(creator_consumer=self.consumer_profile)
        # Check the consumer can access this report
        self.client.login(username="test_consumer2", password="consumerpass2")
        url = reverse("reports_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/reports.html")

    #passes
    def test_reports_view_allows_seller_owner(self):
        report = self.create_report(creator_consumer=self.consumer_profile, posting=self.bundle_posting)
        self.client.login(username="test_seller2", password="sellerpass2")
        url = reverse("reports_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/reports.html")

    # ---------------------------------------------------------------------------

    #Tests for report_view(id)
    #passes
    def test_report_view_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("report_view_url", args=[1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)
    
    #passes
    def test_report_view_allows_consumer_creator(self):
        '''Consumers should be able to view their own reports'''
        # Create a new IssueReport
        report = IssueReport.objects.create(
        posting=self.bundle_posting,
        consumer=self.consumer_profile,
        description="Test"
    )
        # logging in as the owner of the report
        self.client.login(username="test_consumer2", password="consumerpass2")
        url = reverse("report_view_url", args=[report.id])
        response = self.client.get(url)

        # checking response code and template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/report_view.html")
    
    def test_report_view_forbids_other_consumer(self):
        '''Consumers can't view reports created by other consumers'''

        # creating a different consumer
        other_user = User.objects.create_user(
            username="other_consumer", password="pass", user_type="consumer"
        )
        other_profile = Consumer.objects.create(user=other_user)

        # creating a new IssueReport belonging to our mock consumer
        report = IssueReport.objects.create(
            posting=self.bundle_posting,
            consumer=self.consumer_profile,
            description="Test"
        )

        # logging in as the new consumer, who didn't write the IssueReport
        self.client.login(username="other_consumer", password="pass")
        url = reverse("report_view_url", args=[report.id])
        response = self.client.get(url)

        # the new consumer shouldn't be able to access the mock consumer's report
        self.assertEqual(response.status_code, 403)
    
    #passes
    def test_report_view_allows_seller_owner(self):
        '''Seller can view reports for their bundles'''
        # creating a new IssueReport for the mock bundle 
        report = IssueReport.objects.create(
            posting=self.bundle_posting,
            consumer=self.consumer_profile,
            description="Test"
        )

        # logging in as the seller who owns that bundle
        self.client.login(username="test_seller2", password="sellerpass2")
        url = reverse("report_view_url", args=[report.id])
        response = self.client.get(url)

        # checking response code and template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/report_view.html")

    # passes
    def test_report_view_forbids_non_owner_seller(self):
        '''Testing that non-owner sellers cannot access reports for bundles created by other sellers'''

        # creating another seller who isn't the owner of the bundle for which the report was made
        other_user = User.objects.create_user(
            username="other_seller", password="pass", user_type="seller"
        )
        other_profile = Seller.objects.create(
            user=other_user,
            location="X",
            opening_time="09:00",
            closing_time="17:00",
            telephone_number="0",
            website_url="https://x"
        )

        # creating a report for the mock bundle
        report = IssueReport.objects.create(
            posting=self.bundle_posting,
            consumer=self.consumer_profile,
            description="Test"
        )

        # logging in as the non-owner seller
        self.client.login(username="other_seller", password="pass")
        url = reverse("report_view_url", args=[report.id])
        response = self.client.get(url)

        # the non-owner Seller should be forbidden from accessing the report
        self.assertEqual(response.status_code, 403)
    
    #passes
    def test_report_view_seller_can_update_report(self):
        '''The Seller that created the bundle that a report is associated with, should be able to post updates to that report'''
        # creating a new IssueReport
        report = IssueReport.objects.create(
            posting=self.bundle_posting,
            consumer=self.consumer_profile,
            description="Old description"
        )

        # logging in as the mock seller
        self.client.login(username="test_seller2", password="sellerpass2")
        url = reverse("report_view_url", args=[report.id])

        # updating the description
        response = self.client.post(url, {
            "description": "Updated description",
            "type": report.type,
            "status": report.status,
            "seller_response" : "Updated response",
        })

        self.assertEqual(response.status_code, 302)  # redirect after save
        report.refresh_from_db()
        self.assertEqual(report.description, "Updated description")
        self.assertEqual(report.seller_response, "Updated response")
    
    # ---------------------------------------------------------------------------

    #Tests for accessibility_view

    # We need to implement accessibility_view

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

    # Need to implement the logic for this

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

    # Need to implement the logic for this

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


    # ---------------------------------------------------------------------------

class testConsumerOnlyPages(TestCase):

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

        # Create a seller user and their profile
        self.seller_user = User.objects.create_user(
            username="seller1",
            password="sellerpass",
            user_type="seller"
        )
        
        self.seller_profile = Seller.objects.create(
            user=self.seller_user,
            location="Test Location",
            opening_time="09:00",
            closing_time="17:00",
            telephone_number="123456789",
            website_url="https://example.com"
        )

        # Create a consumer user and their profile
        self.consumer_user = User.objects.create_user(
            username="consumer1",
            password="consumerpass",
            user_type="consumer"
        )
        self.consumer_profile = Consumer.objects.create(
            user=self.consumer_user
        )

        # Create a bundle owned by the seller
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
        

    #Tests for report_new_view

    #passes
    def test_report_new_view_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("report_new_view_url", args=[self.bundle_posting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)
    
    #passes
    def test_report_new_view_allows_consumer(self):
        """Consumers should get 200 OK"""
        self.client.login(username="consumer1", password="consumerpass")
        url = reverse("report_new_view_url", args=[self.bundle_posting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    #passes
    def test_report_new_view_allows_seller(self):
        """Sellers shoud get 403 Forbidden"""
        self.client.login(username="seller1", password="sellerpass")
        url = reverse("report_new_view_url", args=[self.bundle_posting.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

        # ---------------------------------------------------------------------------

    #Tests for impact_view

    #passes
    def test_impact_view_redirects_for_anonymous(self):
        """Anonymous users should get 302 Redirect and be redirected to login"""
        url = reverse("impact_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login", response.url)
    
    #passes
    def test_impact_view_allows_consumer(self):
        """Consumers should get 200 OK"""
        self.client.login(username="consumer1", password="consumerpass")
        url = reverse("impact_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    #passes
    def test_impact_view_forbidden_for_seller(self):
        """Sellers shoud get 200 OK"""
        self.client.login(username="seller1", password="sellerpass")
        url = reverse("impact_view_url")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)