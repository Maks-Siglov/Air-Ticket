from django.contrib import auth, messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseRedirect
)
from django.shortcuts import redirect, render

from customer.models import Contact
from users.forms import RegisterForm, UserForm


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


def login(request: HttpRequest) -> HttpResponseRedirect | HttpResponse:
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
                return redirect("customer:profile")
    else:
        form = AuthenticationForm()

    return render(request, "users/login.html", {"form": form})


@login_required(login_url="users:login")
def logout(request: HttpRequest) -> HttpResponseRedirect:
    auth.logout(request)
    messages.success(request, "You are logged out")
    return redirect("main:index")


@login_required(login_url="users:login")
def change_password(
    request: HttpRequest,
) -> HttpResponseRedirect | HttpResponse:
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "You password successfully changed.")
            return redirect("customer:profile")
    else:
        form = PasswordChangeForm(request.user)
    return render(request, "users/change_password.html", {"form": form})


@login_required(login_url="users:login")
def change_contact(
    request: HttpRequest,
) -> HttpResponseRedirect | HttpResponse:
    user = request.user
    if request.method == "POST":
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            contact = Contact.objects.filter(email=user.email).first()
            if contact is not None:
                contact.phone_number = form.cleaned_data["phone_number"]
                contact.save()

            messages.success(request, "You successfully update contacts.")
            return redirect("customer:profile")
    else:
        form = UserForm(instance=user)

    return render(request, "users/change_contact.html", {"form": form})
