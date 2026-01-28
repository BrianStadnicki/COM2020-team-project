from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import SellerExtraForm, GenericSignupForm
from django.template.loader import get_template
from django.template import Context
from .models import User

def testView(request):
    return render(request, "main/test.html")

########### register here ##################################### 
def registerUser(request):
    if request.method == 'POST':
        form = GenericSignupForm(request.POST)
        if form.is_valid():
            user = form.save() #returns custom user instance

            if user.user_type == "seller":
                return redirect("seller-extra", user_id=user.id)
            else:
                #user = User.objects.create_user(form.cleaned_data.get("username"),form.cleaned_data("email"),form.cleaned_data("password1"),form.cleaned_data["user_type"],form.cleaned_data("password2")),
                messages.success(request, f'Your account has been created! You are now able to log in')
                return redirect("login")
        else:
            messages.info(request, f'Check your details.')
            form = GenericSignupForm()
            return render(request, 'registration/signup.html', {'form': form, 'title':'register here'})
    else:
        form = GenericSignupForm()
        return render(request, 'registration/signup.html', {'form': form, 'title':'register here'})
            


def sellerExtra(request, user_id):
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        form = SellerExtraForm(request.POST)
        if form.is_valid():
            seller = form.save(commit=False)
            seller.user_id = user_id
            seller.save()
            form.save_m2m()
            messages.success(request, "Seller profile completed!")
            return redirect("login")
    else:
        form = SellerExtraForm()
    return render(request, "registration/seller_extra.html", {"form":form})
