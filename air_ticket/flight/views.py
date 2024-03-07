from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from flight.forms import FlightForm
from flight.models import Flight
from flight.selectors import get_searched_flights


def search_flights(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            departure_airport = form.cleaned_data["departure_airport"]
            arrival_airport = form.cleaned_data["arrival_airport"]
            departure_date = form.cleaned_data["departure_date"]
            passenger_amount = form.cleaned_data["passenger_amount"]

            page = request.GET.get("page", settings.DEFAULT_PAGE)

            flights = get_searched_flights(
                departure_airport, arrival_airport, departure_date
            )

            paginator = Paginator(flights, settings.FLIGHTS_PER_PAGE)
            current_page = paginator.page(int(page))

            return render(
                request,
                "flight/flight_list.html",
                {
                    "flights": current_page,
                    "flights_count": flights.count(),
                    "departure_airport": departure_airport,
                    "arrival_airport": arrival_airport,
                    "departure_date": departure_date,
                    "passenger_amount": passenger_amount,
                },
            )

    return HttpResponse(status=400)


@login_required(login_url="users:login")
def flight_detail(request: HttpRequest, flight_pk: int):
    try:
        flight = Flight.objects.get(pk=flight_pk)
    except ObjectDoesNotExist:
        messages.warning(request, "Flight does not exist")
        return redirect(request.META.get("HTTP_REFERER"))

    return render(request, "flight/detail.html", {"flight": flight})
