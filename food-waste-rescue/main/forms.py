from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Seller

class GenericSignupForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPES)
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Display Name"}))  
    email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Email"}))  
 
    class Meta:  
        model = User 
        fields = ['user_type', 'username', 'email','password1', 'password2'] 
 
class SellerExtraForm(forms.ModelForm):  
    #location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Location"}))
    #opening_time = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Opening Time"}))
    #closing_time = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Closing Time"}))
    #telephone_number = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Telephone Number"}))
    #website_URL = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Website URL"}))
 
    class Meta:  
        model = Seller
        fields = ['location','opening_time','closing_time','telephone_number','website_url']  