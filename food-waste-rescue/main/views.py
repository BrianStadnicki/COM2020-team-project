from urllib import request
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django import forms
# from .forms import ...

def test_view(request):
    return render(request, "main/test.html")

def home_view(request):
    return render(request, "main/home.html")

def bundles_view(request):
    return render(request, "main/bundles.html")

def reservations_view(request):
    return render(request, "main/reservations.html")

# Seller Views
def seller_view(request):
    return render(request, "main/seller.html")

def seller_profile_view(request):
    return render(request, "main/seller_profile.html") 

def seller_reports_view(request):
    return render(request, "main/seller_reports.html")

def seller_response_view(request):
    
    # Temporary form until created forms can be imported 
    form_class = forms.Form
    form = form_class()
    # 
    
    if request.method == "POST":   
        form = form_class(request.POST)  
        if form.is_valid():
            # form.save() and/or something else
            pass
    else: 
        form = form_class()
    return render(request, "main/seller_response.html") # , {"form":form}

def seller_accessibility_view(request):
    return render(request, "main/seller_accessibility.html")

def seller_bundles_view(request):
    return render(request, "main/seller_bundles.html")

def seller_create_bundles_view(request):
    
    # Temporary form until created forms can be imported 
    form_class = forms.Form
    form = form_class()
    # 
    
    if request.method == "POST":   
        form = form_class(request.POST)  
        if form.is_valid():
            # form.save() and/or something else
            pass
    else: 
        form = form_class()
    
    return render(request, "main/seller_create_bundles.html") #, {"form":form}

def seller_finalise_bundles_view(request):

    # Temporary form until created forms can be imported 
    form_class = forms.Form
    form = form_class()
    # 
    
    if request.method == "POST":   
        form = form_class(request.POST)  
        if form.is_valid():
            # form.save() and/or something else
            pass
    else: 
        form = form_class()

    return render(request, "main/seller_finalise_bundles.html") #, {"form":form}

def seller_reservations_view(request):
    return render(request, "main/seller_reservations.html")

def seller_analytics_view(request):
    return render(request, "main/seller_analytics.html")

def seller_activity_view(request):
    return render(request, "main/seller_activity.html")

# Consumer Views

def consumer_view(request):
    return render(request, "main/consumer.html")

def consumer_profile_view(request):
    return render(request, "main/consumer_profile.html") 

def consumer_accessibility_view(request):
    return render(request, "main/consumer_accessibility.html")

def consumer_impact_view(request):
    return render(request, "main/consumer_impact.html")

def consumer_details_view(request):
    
    # Temporary form until created forms can be imported 
    form_class = forms.Form
    form = form_class()
    # 
    
    if request.method == "POST":   
        form = form_class(request.POST)  
        if form.is_valid():
            # form.save() and/or something else
            pass
    else: 
        form = form_class()    
    
    return render(request, "main/consumer_details.html") #, {"form":form}

def consumer_bundles_view(request):
    return render(request, "main/consumer_bundles.html")

def consumer_reservations_view(request):
    return render(request, "main/consumer_reservations.html")

def consumer_reports_view(request):
    return render(request, "main/consumer_reports.html")

# Developer Views

def developer_view(request):
    return render(request, "main/developer.html")

def developer_reports_view(request):
    return render(request, "main/developer_reports.html")

def developer_company_view(request):
    return render(request, "main/developer_company.html")

def developer_developer_company_view(request):
    return render(request, "main/developer_developer_company.html")