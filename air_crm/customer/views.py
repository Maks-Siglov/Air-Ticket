from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


@login_required(login_url="users:login")
def profile(request: HttpRequest) -> HttpResponse:
    return render(request, "customer/profile.html")
