from flight.models import Airport
from rest_framework import serializers


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("name",)
