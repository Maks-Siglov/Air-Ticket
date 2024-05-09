from rest_framework import serializers

from customer.models import Contact


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ("phone_number", "email")
