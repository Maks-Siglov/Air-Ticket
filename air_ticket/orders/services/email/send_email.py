from django.core.mail import EmailMultiAlternatives


def send_tickets_email(html_content: str, user_email: str) -> None:

    mail = EmailMultiAlternatives(
        subject="AirTicket",
        body=html_content,
        from_email="etqueens22@gmail.com",
        to=[user_email],
    )
    mail.attach_alternative(html_content, "text/html")

    mail.send()
