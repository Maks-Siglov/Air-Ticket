from django.http import HttpResponse, HttpRequest
from django.shortcuts import render

from flight.forms import FlightForm
from flight.selectors import get_searched_flights


def search_flights(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = FlightForm(request.POST)
        if form.is_valid():
            departure_airport = form.cleaned_data['departure_airport']
            destination_airport = form.cleaned_data['destination_airport']
            departure_date = form.cleaned_data['departure_date']
            passenger_amount = form.cleaned_data['passenger_amount']

            flights = get_searched_flights(
                departure_airport, destination_airport, departure_date
            )

            return render(
                request,
                "flight/flight_list.html",
                {
                    "flights": flights,
                    "flights_count": flights.count(),
                    "departure_airport": departure_airport,
                    "destination_airport": destination_airport,
                    "departure_date": departure_date,
                    "passenger_amount": passenger_amount,
                }
            )
