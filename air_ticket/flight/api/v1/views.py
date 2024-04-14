from django.http import HttpRequest

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from flight.api.v1.serializers import AirportSerializer, FlightSerializer
from flight.forms import FlightForm
from flight.selectors import get_searched_flights, get_suggestion_airports


class SearchFlightsAPIView(APIView):
    def post(self, request: HttpRequest, *args, **kwargs) -> Response:
        form = FlightForm(request.data)
        if form.is_valid():
            departure_city = form.cleaned_data["departure_airport"]
            arrival_city = form.cleaned_data["arrival_airport"]
            departure_date = form.cleaned_data["departure_date"]
            passenger_amount = form.cleaned_data["passenger_amount"]

            flights = get_searched_flights(
                departure_city, arrival_city, departure_date
            )
            serialized_flights = FlightSerializer(flights, many=True)

            response = {
                "passenger_amount": passenger_amount,
                "flights_count": flights.count(),
                "departure_city": departure_city,
                "arrival_city": arrival_city,
                "departure_date": departure_date,
                "flights": serialized_flights.data,
            }

            return Response(response)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class SuggestAirportAPIView(APIView):
    def get(self, request: HttpRequest, value: str) -> Response:
        airports = get_suggestion_airports(value)

        if not airports.exists():
            return Response(status=204)

        serializer = AirportSerializer(airports, many=True)
        return Response(serializer.data, status=200)
