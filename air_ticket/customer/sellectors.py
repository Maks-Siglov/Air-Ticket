from customer.models import Contact


def get_contact(contact_pk: int) -> Contact:
    return Contact.objects.get(pk=contact_pk)
