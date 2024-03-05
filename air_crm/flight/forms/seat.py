from django import forms

from flight.models import Seat


class SeatForm(forms.ModelForm):
    class Meta:
        model = Seat
        fields = ('type',)
