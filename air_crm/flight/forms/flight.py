from django import forms

from flight.models import Flight


class FlightForm(forms.ModelForm):
    passenger_amount = forms.IntegerField()

    class Meta:
        model = Flight
        fields = (
            "departure_airport",
            "destination_airport",
            "departure_date",
            "passenger_amount"
        )
