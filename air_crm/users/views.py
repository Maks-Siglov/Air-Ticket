from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect

from users.forms import RegisterForm


def register(request: HttpRequest) -> HttpResponse | HttpResponseRedirect:
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account successfully register")
            return redirect("users:login")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", {"form": form})


def login(request: HttpRequest) -> HttpResponseRedirect:
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = auth.authenticate(
                request, username=email, password=password
            )
            if user is not None:
                auth.login(request, user)
                messages.success(request, "You are log in")
                return redirect("main:index")
    else:
        form = AuthenticationForm()

    return render(request, "users/login.html", {"form": form})
