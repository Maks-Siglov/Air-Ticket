from rest_framework import serializers

from customer.models import Passenger


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ("first_name", "last_name", "passport_id")
