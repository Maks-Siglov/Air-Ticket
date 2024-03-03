from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from flight.forms import FlightForm
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
