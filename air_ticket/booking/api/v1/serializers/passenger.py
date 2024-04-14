from customer.models import Passenger
from rest_framework import serializers


class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = ("first_name", "last_name", "passport_id")
