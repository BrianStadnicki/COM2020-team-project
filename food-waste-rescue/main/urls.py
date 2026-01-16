from django.urls import path
from . import views

urlpatterns = [
    path('test/', views.testView, name='test_view_url')
]
