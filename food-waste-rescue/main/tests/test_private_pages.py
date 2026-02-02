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
