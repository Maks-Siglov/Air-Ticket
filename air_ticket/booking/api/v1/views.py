from datetime import timedelta

from django.conf import settings
from django.db import IntegrityError, transaction
from django.utils import timezone

from rest_framework import status
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from booking.api.v1.serializers import (
    ContactSerializer,
    PassengerSerializer,
    TicketSerializer,
)
from booking.models import Booking, Ticket, TicketCart
from booking.selectors import get_cart, get_first_booking, get_ticket
from customer.models import Contact
from customer.sellectors import get_contact


class CreateTicketCartAPI(CreateAPIView):
    def get_object(self) -> TicketCart | Response:
        cart_pk = self.kwargs.get("cart_pk")
        if cart_pk is None:
            return Response(
                {"error": "Cart ID not provided in URL"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if (cart := get_cart(cart_pk)) is None:
            return Response(
                {"error": "Cart does not exits"}, status.HTTP_404_NOT_FOUND
            )
        return cart

    def create(self, request: Request, *args, **kwargs) -> Response:
        cart = self.get_object()
        if (booking := get_first_booking(cart)) is None:
            return Response(
                {"error": "Booking does not exists"}, status.HTTP_404_NOT_FOUND
            )

        passenger_serializer = PassengerSerializer(data=request.data)
        ticket_serializer = TicketSerializer(data=request.data)

        if not (
            passenger_serializer.is_valid() and ticket_serializer.is_valid()
        ):
            return Response(
                {"error": "Provided data not valid"},
                status.HTTP_400_BAD_REQUEST,
            )
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
    def get_object(self) -> Ticket | Response:
        ticket_pk = self.kwargs.get("ticket_pk")
        if ticket_pk is None:
            return Response(
                {"error": "Ticket ID not provided in URL"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if (ticket := get_ticket(ticket_pk)) is None:
            return Response("Ticket does not exist", status.HTTP_404_NOT_FOUND)
        return ticket

    def update(self, request: Request, *args, **kwargs) -> Response:
        ticket = self.get_object()
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
            return Response(
                {"Error": "Provided data not valid"},
                status.HTTP_400_BAD_REQUEST,
            )

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
    def get_object(self) -> TicketCart | Response:
        cart_pk = self.kwargs.get("cart_pk")
        if cart_pk is None:
            return Response(
                {"error": "Cart ID not provided in URL"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if (cart := get_cart(cart_pk)) is None:
            return Response(
                {"error": "Cart does not exits"}, status.HTTP_404_NOT_FOUND
            )
        return cart

    def create(self, request: Request, *args, **kwargs) -> Response:
        cart = self.get_object()
        contact_serializer = ContactSerializer(data=request.data)
        if contact_serializer.is_valid():
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
        return Response(
            {"error": "Provided data not valid"}, status.HTTP_400_BAD_REQUEST
        )


class UpdateContactAPI(UpdateAPIView):
    def get_object(self) -> Contact | Response:
        contact_pk = self.kwargs.get("contact_pk")
        if contact_pk is None:
            return Response(
                {"error": "Cart ID not provided in URL"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if (contact := get_contact(contact_pk=contact_pk)) is None:
            return Response(
                {"error": "Contact does not exits"}, status.HTTP_404_NOT_FOUND
            )
        return contact

    def update(self, request: Request, *args, **kwargs) -> Response:
        contact_serializer = ContactSerializer(
            data=request.data, instance=self.get_object()
        )
        if not contact_serializer.is_valid():
            return Response(
                {"Error": contact_serializer.errors},
                status.HTTP_400_BAD_REQUEST,
            )
        contact_serializer.save()

        return Response(
            {
                "success": "Contact updated",
                "contact": contact_serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )


class DeleteExpiredBookingAPI(APIView):
    def post(self, request: Request) -> Response:
        threshold_time = timezone.now() - timedelta(
            minutes=settings.BOOKING_MINUTES_LIFETIME
        )

        expired_bookings = Booking.objects.filter(
            ticket=None, created_at__lte=threshold_time
        )
        if expired_bookings.exists():
            expired_bookings.delete()
            return Response(
                "Expired bookings have been deleted.",
                status.HTTP_204_NO_CONTENT,
            )

        return Response("There is no Expired bookings", status.HTTP_200_OK)
