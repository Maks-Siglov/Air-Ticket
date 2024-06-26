from customer.models import Contact


def get_contact(contact_pk: int) -> Contact | None:
    return Contact.objects.filter(pk=contact_pk).first()


def get_contact_by_email(email: str) -> Contact | None:
    return Contact.objects.filter(email=email).first()
