from rest_framework import serializers

from flight.models import Seat


class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ("id", "type", "is_available")
