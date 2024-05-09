from rest_framework import serializers

from flight.models import Airport


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("name",)
