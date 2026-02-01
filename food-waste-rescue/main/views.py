from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django import forms

def test_view(request):
    return render(request, "main/test.html")

"""
Consumer: Show all bundles, search by location and pick up time, pagination
Seller: Show own bundles, pagination
"""
def bundles_view(request):
    return render(request, "main/bundles.html")

"""
Consumer: Show bundle, make new reservation or view own reservation details
Seller: show/edit/delete bundle, change reservation status?
"""
def bundle_view(request, id):
    return render(request, "main/bundle.html")

"""
Seller: create new bundle
"""
def bundle_new_view(request):
    return render(request, "main/bundle_new.html")

"""
Seller: See analytics, actually create
"""
def bundle_confirm_view(request):
    return render(request, "main/bundle_confirm.html")

"""
Consumer: Show own reservations with bundle details
Seller: Show upcoming reservations with bundle details, edit status, search/verify code
"""
def reservations_view(request):
    return render(request, "main/reservations.html")

"""
Consumer: Show/delete own reservation with bundle details
Seller: Show/edit own reservation with bundle details
"""
def reservation_view(request, id):
    return render(request, "main/reservation.html")

"""
Seller: Show analytics
"""
def analytics_view(request):
    return render(request, "main/analytics.html")

"""
Consumer: Show own reports
Seller: Show own reports
"""
def reports_view(request):
    return render(request, "main/reports.html")

"""
Consumer: Show/add/close own report
Seller: Show/add/close own report
"""
def report_view(request, id):
    return render(request, "main/report.html")

"""
Consumer: Create new report
Seller: Create new report
"""
def report_new_view(request):
    return render(request, "main/report_new.html")

"""
Consumer: View impact
Seller: View impact
"""
def impact_view(request):
    return render(request, "main/impact.html")

"""
Consumer: View/Change accessibility settings
Seller: View/Change accessibility settings
"""
def accessibility_view(request):
    return render(request, "main/accessibility.html")
