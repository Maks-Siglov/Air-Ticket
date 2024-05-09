from rest_framework import serializers


class TicketCreationResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    passenger_id = serializers.IntegerField()
    ticket_id = serializers.IntegerField()
