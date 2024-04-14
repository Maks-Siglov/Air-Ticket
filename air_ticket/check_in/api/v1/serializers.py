from flight.models import Seat
from rest_framework import serializers


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ("id",)
