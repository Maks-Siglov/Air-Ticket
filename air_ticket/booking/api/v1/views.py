from datetime import timedelta

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from django.utils import timezone

from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from booking.api.v1.serializers import (
    ContactSerializer,
    PassengerSerializer,
    TicketSerializer,
)
from booking.models import Booking, Ticket
from booking.selectors import get_cart, get_first_booking, get_ticket
from customer.sellectors import get_contact


class CreateTicketCartAPI(APIView):
    def post(self, request: Request, cart_pk: int) -> Response:
        if (cart := get_cart(cart_pk)) is None:
            return Response(
                {"error": "Cart does not exits"}, status.HTTP_404_NOT_FOUND
            )

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


class TicketUpdateAPI(APIView):
    def put(self, request: Request, ticket_pk: int) -> Response:
        if (ticket := get_ticket(ticket_pk)) is None:
            return Response("Ticket does not exist", status.HTTP_404_NOT_FOUND)

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


class ContactAPI(APIView):
    def post(self, request: Request, cart_pk: int) -> Response:
        if (cart := get_cart(cart_pk)) is None:
            return Response(
                {"error": "Cart does not exits"}, status.HTTP_404_NOT_FOUND
            )

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

    def put(self, request: Request, contact_pk: int) -> Response:
        try:
            contact = get_contact(contact_pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": "Contact does not exist"}, status.HTTP_404_NOT_FOUND
            )

        contact_serializer = ContactSerializer(
            data=request.data, instance=contact
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
