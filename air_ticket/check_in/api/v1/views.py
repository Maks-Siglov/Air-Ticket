from django.http import HttpRequest
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response

from check_in.api.v1.serializers import SeatSerializer
from flight.models import Seat


class SeatsView(APIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Seat.objects.all()

    def get(
        self, request: HttpRequest, flight_pk: int, format=None
    ) -> Response:
        seats = self.queryset.filter(airplane__flight__pk=flight_pk)
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)
