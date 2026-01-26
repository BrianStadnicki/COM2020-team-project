from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.template.loader import get_template
from django.template import Context

def testView(request):
    return render(request, "main/test.html")

########### register here ##################################### 
def registerUser(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user_type = form.cleaned_data.get("user_type"),
            display_name=form.cleaned_data("display_name"),  
            email=form.cleaned_data("email"),  
            password=form.cleaned_data("password"),
            confirm_password=form.cleaned_data("confirm_password"),
            messages.success(request, f'Your account has been created! You are now able to log in')
            return redirect('login')
        else:
            messages.info(request, f'Check your details.')
    form = UserRegisterForm()
    return render(request, 'user/register.html', {'form': form, 'title':'register here'})
 

'''
def save(self, request):  
        # Save the user first  
        user = super().save(request)  
        user.save()  
 
        # Create a PrivateProfile linked to the user  
        user.objects.create(  
            user=user,  
            display_name=self.cleaned_data["display_name"],  
            email=self.cleaned_data["email"],  
            password=self.cleaned_data["password"],
        )  
        return user

def save(self, request):  
        # Save the user first  
        user = super().save(request)  
        user.save()  
 
        # Create a PrivateProfile linked to the user  
        user.objects.create(  
            user=user,  
            location=self.cleaned_data["location"],
            opening_time=self.cleaned_data["opening_time"],
            closing_time=self.cleaned_data["closing_time"],
            telephone_number=self.cleaned_data["telephone_number"],
            website_URL=self.cleaned_data["website_URL"],
        )  
        return user
'''