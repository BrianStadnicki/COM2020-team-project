from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import SellerExtraForm, UserRegisterForm
from django.template.loader import get_template
from django.template import Context

def testView(request):
    return render(request, "main/test.html")

########### register here ##################################### 
def registerUser(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save() #returns custom user instance

            if user.user_type == "seller":
                return redirect("seller-extra", user_id=user.id)
            else:
                Consumer.objects.create(user=user)
                messages.success(request, "Account created!")
                user_type = form.cleaned_data["user_type"],
                display_name=form.cleaned_data.get("display_name"),  
                email=form.cleaned_data("email"),  
                password=form.cleaned_data("password"),
                confirm_password=form.cleaned_data("confirm_password"),
                messages.success(request, f'Your account has been created! You are now able to log in')
                return redirect("login")
        else:
            messages.info(request, f'Check your details.')
            form = UserRegisterForm()
            return render(request, 'user/register.html', {'form': form, 'title':'register here'})

def sellerExtra(request, user_id):
    user = user.objects.get(id=user_id)
    if request.method == "POST":
        form = SellerExtraForm(request.POST)
        if form.is_valid():
            seller = form.save()
            messages.success(request, "Seller profile completed!")
            return redirect("login")
    else:
        form = SellerExtraForm()
    return render(request, "user/seller_extra.html", {"form":form})
