
from django.shortcuts import render,redirect
from .forms import UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate

# Create your views here.

def signup_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f'Account successfully created for {username}!, You can login into your account now')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, "accounts/register.html", {"form": form})



