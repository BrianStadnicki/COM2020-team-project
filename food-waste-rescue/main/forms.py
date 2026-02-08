from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import Seller
from .models import Bundle_posting, IssueReport, Reservation

class GenericSignupForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=User.USER_TYPES)
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Display Name"}))  
    email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Email"}))  
 
    class Meta:  
        model = User 
        fields = ['user_type', 'username', 'email','password1', 'password2'] 
 
class SellerExtraForm(forms.ModelForm):  
    class Meta:  
        model = Seller
        fields = ['location','opening_time','closing_time','telephone_number','website_url']  

class BundleNewForm(forms.ModelForm):
    class Meta:
        model = Bundle_posting
        fields = ['name', 'category', 'quantity', 'price', 'pickup_window_start', 'pickup_window_end', 'allergen_celery', 'allergen_crustacean', 'allergen_dairy', 'allergen_egg', 'allergen_fish', 'allergen_gluten', 'allergen_lupin', 'allergen_mollusc', 'allergen_mustard', 'allergen_nut', 'allergen_peanut', 'allergen_sesame', 'allergen_soya', 'allergen_sulphite', 'contents_description']

class IssueReportNewForm(forms.ModelForm):
    class Meta:
        model = IssueReport
        fields = ['type','description']

class IssueReportViewForm(forms.ModelForm):
    class Meta:
        model = IssueReport
        fields = ['type', 'description', 'seller_response', 'status']

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['id', 'status']

class BundleDeleteForm(forms.ModelForm):
    class Meta:
        model = Bundle_posting
        fields = []
