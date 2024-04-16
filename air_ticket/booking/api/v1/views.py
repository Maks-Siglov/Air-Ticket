from datetime import timedelta

from django.conf import settings
from django.db import IntegrityError, transaction
from django.utils import timezone

from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from booking.api.v1.serializers import (
    ContactSerializer,
    PassengerSerializer,
    TicketSerializer,
)
from booking.crud import get_cart, get_first_booking, get_ticket
from booking.models import Booking, Ticket, TicketCart
from customer.crud import get_contact
from customer.models import Contact


class CreateTicketCartAPI(CreateAPIView):
    http_method_names = ["post"]

    def get_object(self, cart_pk: int) -> TicketCart | Response:
        if (cart := get_cart(cart_pk)) is None:
            raise NotFound(detail="Cart not found")
        return cart

    def create(self, request: Request, cart_pk: int) -> Response:
        cart = self.get_object(cart_pk)
        if (booking := get_first_booking(cart)) is None:
            raise NotFound(detail="Booking not found")

        passenger_serializer = PassengerSerializer(data=request.data)
        ticket_serializer = TicketSerializer(data=request.data)

        if not (
            passenger_serializer.is_valid() and ticket_serializer.is_valid()
        ):
            raise ValidationError(detail="Provided data not valid")
        try:
            with transaction.atomic():
                passenger = passenger_serializer.save()
                ticket_data = ticket_serializer.validated_data
                ticket_data["passenger"] = passenger
                ticket_data["cart"] = cart
                ticket = Ticket.objects.create(**ticket_data)

                booking.ticket = ticket
                booking.save()
        except IntegrityError:
            return Response(
                {"error": "Try again later"}, status.HTTP_409_CONFLICT
            )

        return Response(
            {
                "message": "Ticket successfully created",
                "passenger": passenger_serializer.data,
                "ticket": ticket_serializer.data,
            },
            status.HTTP_201_CREATED,
        )


class TicketUpdateAPI(UpdateAPIView):
    http_method_names = ["put"]

    def get_object(self, ticket_pk: int) -> Ticket | Response:
        if (ticket := get_ticket(ticket_pk)) is None:
            raise NotFound(detail="Ticket not found")
        return ticket

    def update(self, request: Request, ticket_pk: int) -> Response:
        ticket = self.get_object(ticket_pk)
        passenger = ticket.passenger
        ticket_serializer = TicketSerializer(
            data=request.data, instance=ticket
        )
        passenger_serializer = PassengerSerializer(
            data=request.data, instance=passenger
        )

        if not (
            passenger_serializer.is_valid() and ticket_serializer.is_valid()
        ):
            raise ValidationError(detail="Provided data not valid")

        try:
            with transaction.atomic():
                ticket_serializer.save()
                passenger_serializer.save()
        except IntegrityError:
            return Response(
                {"error": "Try again later"}, status.HTTP_409_CONFLICT
            )

        return Response(
            {
                "message": "Ticket successfully updated",
                "passenger": passenger_serializer.data,
                "ticket": ticket_serializer.data,
            },
            status.HTTP_201_CREATED,
        )


class CreateContactAPI(CreateAPIView):
    serializer_class = ContactSerializer
    http_method_names = ["post"]

    def get_object(self, cart_pk: int) -> TicketCart | Response:
        if (cart := get_cart(cart_pk)) is None:
            raise NotFound(detail="Cart not found")
        return cart

    def create(self, request: Request, cart_pk: int) -> Response:
        cart = self.get_object(cart_pk)
        contact_serializer = self.serializer_class(data=request.data)
        if not contact_serializer.is_valid():
            raise ValidationError(detail="Provided data not valid")
        contact = contact_serializer.save()
        cart.contact = contact
        cart.save()

        return Response(
            {
                "success": "Contact created",
                "contact": contact_serializer.data,
            },
            status.HTTP_201_CREATED,
        )


class UpdateContactAPI(UpdateAPIView):
    serializer_class = ContactSerializer
    http_method_names = ["put"]

    def get_object(self, contact_pk: int) -> Contact | Response:
        if (contact := get_contact(contact_pk=contact_pk)) is None:
            raise NotFound(detail="Contact not found")
        return contact

    def update(self, request: Request, contact_pk: int) -> Response:
        contact_serializer = self.serializer_class(
            data=request.data, instance=self.get_object(contact_pk)
        )
        if not contact_serializer.is_valid():
            raise ValidationError(detail="Provided data not valid")

        contact_serializer.save()
        return Response(
            {
                "success": "Contact updated",
                "contact": contact_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class DeactivateExpiredBookingAPI(APIView):
    def post(self, request: Request) -> Response:
        threshold_time = timezone.now() - timedelta(
            minutes=settings.BOOKING_MINUTES_LIFETIME
        )

        expired_bookings = Booking.objects.filter(
            ticket=None, created_at__lte=threshold_time
        )
        if not expired_bookings.exists():
            return Response("There is no Expired bookings", status.HTTP_200_OK)

        expired_bookings.update(is_active=False)

        return Response(
            "Expired bookings have been deactivated.",
            status.HTTP_204_NO_CONTENT,
        )
