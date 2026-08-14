from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from wallet.models import Wallet

from .forms import LoginForm, RegisterForm

# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")
    form = LoginForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(request,email=email,password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Welcome back!")
                return redirect("home")
            messages.error(request, "Invalid email or password.")
    return render(request,"registration/login.html",{"form": form})

def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard:index")

    if request.method == "POST":
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user=form.save()
            Wallet.objects.create(
            user=user,
            balance=0,
            reserved_balance=0,
            total_deposited=0,
            total_withdrawn=0
        )
            login(request,user)
            messages.success(request,"Account created successfully. You can now login.")
            return redirect("dashboard")
    else:
        form = RegisterForm()
    context = {
        "form": form
    }
    return render(request,'registration/register.html',context)

@login_required
def logout_view(request):
    logout(request)
    messages.success(request,"Logged out successfully.")
    return redirect("login")

@login_required
def settings_view(request):
    return render(request,"accounts/settings.html")