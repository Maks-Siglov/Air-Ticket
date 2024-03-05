from django import forms

from booking.models import Ticket
from flight.models import Seat


class TicketForm(forms.ModelForm):
    seat_type = forms.ChoiceField(choices=Seat.TYPE_CHOICES)

    class Meta:
        model = Ticket
        fields = ("price", "lunch", "luggage", "seat_type")
