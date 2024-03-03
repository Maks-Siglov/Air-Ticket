from django import forms

from booking.models import Ticket


class TicketForm(forms):
    class Meta:
        model = Ticket
        fields = ("price", )
