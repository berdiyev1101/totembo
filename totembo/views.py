from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import ListView

from totembo.forms import SignUpForm, SignInForm


# class Index(ListView):
#     template_name = "totembo/index.html"

def index(request):
    return render(request,"totembo/index.html")


def signup(request):
    form = SignUpForm(data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password1")
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect("index")
    context = {
        "title":"Sign Up",
        "form":form
    }
    return render(request,"totembo/signup.html",context)


def signin(request):
    form = SignInForm(data=request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password")
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect("index")
    context = {
        "title":"Sign In",
        "form":form
    }
    return render(request,"totembo/signin.html",context)

def signout(request):
    logout(request)
    return redirect("signin")



