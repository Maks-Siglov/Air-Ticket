from rest_framework import serializers


class ContactCreationResponseSerializer(serializers.Serializer):
    message = serializers.CharField()
    contact_id = serializers.IntegerField()
