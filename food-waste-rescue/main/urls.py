from django.urls import include, path
from . import views

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("test/", views.testView, name="test_view_url"),
    path('accounts/register/', views.registerUser, name="register"),
]
