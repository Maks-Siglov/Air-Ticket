from django import forms

from customer.models import Passenger


class PassengerForm(forms.ModelForm):
    class Meta:
        model = Passenger
        fields = ("passport_id", "first_name", "last_name", "email")
