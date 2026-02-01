from django.urls import include, path
from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("test/", views.test_view, name="test_view_url"),
    path("bundles", views.bundles_view, name="bundles_view_url"),
    path("bundle/<int:id>", views.bundle_view, name="bundle_view_url"),
    path("bundle/new", views.bundle_new_view, name="bundle_new_view_url"),
    path("bundle/confirm", views.bundle_confirm_view, name="bundle_confirm_view_url"),
    path("reservations/", views.reservations_view, name="reservations_view_url"),
    path("reservations/<int:id>", views.reservation_view, name="reservation_view_url"),
    path("analytics/", views.analytics_view, name="analytics_view_url"),
    path("reports/", views.reports_view, name="reports_view_url"),
    path("report/<int:id>", views.report_view, name="report_view_url"),
    path("report/new", views.report_new_view, name="report_new_view_url"),
    path("impact", views.impact_view, name="impact_view_url"),
    path("accessibility", views.accessibility_view, name="accessibility_view_url"),
]
