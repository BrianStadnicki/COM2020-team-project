from django.urls import include, path
from . import views

urlpatterns = [
    
    # main paths
    path("accounts/", include("django.contrib.auth.urls")),
    path("", views.home_view, name="home_view_url"),
    path("test/", views.test_view, name="test_view_url"),
    path("bundles/", views.bundles_view, name="bundles_view_url"),
    path("reservations/", views.reservations_view, name="reservations_view_url"),
    
    #seller paths
    path("seller/", views.seller_view, name="seller_view_url"),
    path("seller/profile/", views.seller_profile_view, name="seller_profile_view_url"),
    path("seller/reports/", views.seller_reports_view, name ="seller_reports_view_url"),
    path("seller/response/", views.seller_response_view, name="seller_response_view_url"),
    path("seller/accessbility/", views.seller_accessibility_view, name="seller_accessibility_view_url"),
    path("seller/bundles/", views.seller_bundles_view, name="seller_bundles_view_url"),
    path("seller/bundles/create/", views.seller_create_bundles_view, name="seller_create_bundles_view_url"),
    path("seller/bundles/finalise", views.seller_finalise_bundles_view, name="seller_finalise_bundles_view_url"),
    path("seller/reservations/", views.seller_reservations_view, name="seller_reservations_view_url"),
    path("seller/analytics/", views.seller_analytics_view, name="seller_analytics_view_url"),
    path("seller/activity/", views.seller_activity_view, name="seller_activity_view_url"),
     
    #consumer paths
    path("consumer/", views.consumer_view, name="consumer_view_url"),
    path("consumer/profile/", views.consumer_profile_view, name="consumer_profile_view_url"),
    path("consumer/accessibility/", views.consumer_accessibility_view, name="consumer_accessibility_view_url"),
    path("consumer/impact/", views.consumer_impact_view, name="consumer_impact_view_url"),
    path("consumer/details/", views.consumer_details_view, name="consumer_details_view_url"),
    path("consumer/bundles/", views.consumer_bundles_view, name="consumer_bundles_view_url"),
    path("consumer/reservations/", views.consumer_reservations_view, name="consumer_reservations_view_url"),
    path("consumer/reports/", views.consumer_reports_view, name="consumer_reports_view_url"),
   
   #developer paths
   path("developer/", views.developer_view, name = "developer_view_url"),
   path("developer/reports/", views.developer_reports_view, name="developer_reports_url"),
   path("developer/company/", views.developer_company_view, name="developer_company_url"),
   path("developer/developer_company", views.developer_developer_company_view, name="developer_developer_company_url")
]