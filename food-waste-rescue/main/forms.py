from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
import models

class GenericSignupForm(UserCreationForm):
    user_type = forms.CharField(max_length=10, choices=models.User.USER_TYPES, default="consumer")
    display_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Display Name"}))  
    email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Email"}))  
    password = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Password"}))
    confirm_password = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Confirm Password"})) 
 
    class Meta:  
        model = User 
        fields = ['user_type','display_name','email','password','confirm_password'] 
 
    
    
class SellerSignupForm(UserCreationForm):  
    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Location"}))
    opening_time = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Opening Time"}))
    closing_time = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Closing Time"}))
    telephone_number = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Telephone Number"}))
    website_URL = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Website URL"}))
 
    class Meta:  
        model = User
        fields = ['user_type','display_name','email','password','confirm_password','location','opening_time','closing_time','telephone_number','website_URL']  