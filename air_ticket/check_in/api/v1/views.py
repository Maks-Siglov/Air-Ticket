from django.http import HttpRequest

from rest_framework.response import Response
from rest_framework.views import APIView

from check_in.api.v1.serializers import SeatSerializer
from flight.models import Seat


class SeatsView(APIView):

    def get(
        self, request: HttpRequest, flight_pk: int, format=None
    ) -> Response:
        seats = Seat.objects.filter(airplane__flight__pk=flight_pk)
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)


class SelectSeatView(APIView):

    def post(self, request: HttpRequest) -> Response:
        seat_pk = request.data["seatId"]
        seat = Seat.objects.get(pk=seat_pk)
        seat.is_available = False
        seat.save()
        return Response(status=200)
