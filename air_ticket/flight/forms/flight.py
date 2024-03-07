from django import forms


class FlightForm(forms.Form):
    passenger_amount = forms.IntegerField()
    arrival_airport = forms.CharField()
    departure_airport = forms.CharField()
    departure_date = forms.DateTimeField()
