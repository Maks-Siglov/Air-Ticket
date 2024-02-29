from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def flights_list(request: HttpRequest) -> HttpResponse: ...
