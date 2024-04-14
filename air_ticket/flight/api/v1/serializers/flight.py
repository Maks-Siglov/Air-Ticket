from flight.models import Flight
from rest_framework import serializers


class FlightSerializer(serializers.ModelSerializer):
    airplane__name = serializers.CharField(source="airplane.name")
    arrival_airport__timezone = serializers.CharField(
        source="arrival_airport.timezone"
    )
    departure_airport__timezone = serializers.CharField(
        source="departure_airport.timezone"
    )
    arrival_airport__name = serializers.CharField(
        source="arrival_airport.name"
    )
    departure_airport__name = serializers.CharField(
        source="departure_airport.name"
    )

    class Meta:
        model = Flight
        fields = (
            "airplane__name",
            "arrival_airport__timezone",
            "departure_airport__timezone",
            "arrival_airport__name",
            "departure_airport__name",
            "departure_scheduled",
            "arrival_scheduled",
        )
