from django import forms

from booking.models import Ticket
from flight.models import Seat


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ("price", "lunch", "luggage")
