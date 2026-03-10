from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class TestPublicPages(TestCase):
    """
    Public pages (expect 200):
    /accounts/login/
    /accounts/register/
    /accounts/registerseller<id>/

    /accounts/registerseller<id>/ : even though only Sellers should ever land 
    on this page, this needs to be public, because the user is not logged in 
    yet during the signup flow.
    Multi-step registration flows must allow public access to the second step.
    Consumers should be blocked from accessing it but that's a logic restriction,
    not an authentication restriction (therefore this needs to be enforced within the
    relevant view).
    """

    #passes
    def test_login_page_is_public(self):
        """
        Testing that the login page is publicly accessible
        """
        response = self.client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    #passes
    def test_register_page_is_public(self):
        """
        Testing that the registration / signup page is publicly accessible (this page 
        should not require the user to be logged in)
        """
        url = reverse("register")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/signup.html")
