from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from flight.api.v1.serializers import FlightSerializer
from flight.forms import FlightForm
from flight.selectors import get_searched_flights


class SearchFlightsAPIView(APIView):
    def post(self, request, *args, **kwargs):
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
