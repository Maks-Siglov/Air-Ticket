from django import forms

from customer.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ("phone_number", "email")
