from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpRequest

from rest_framework.views import APIView
from rest_framework.response import Response

from booking.api.v1.serializers import PassengerSerializer, TicketSerializer
from booking.models import Ticket
from booking.selectors import get_cart, get_ticket


class TicketAPI(APIView):
    def post(self, request: HttpRequest, cart_pk: int) -> Response:
        try:
            cart = get_cart(cart_pk)
        except ObjectDoesNotExist:
            return Response({"error": "Cart does not exits"}, status=404)

        passenger_serializer = PassengerSerializer(data=request.data)
        ticket_serializer = TicketSerializer(data=request.data)

        if passenger_serializer.is_valid() and ticket_serializer.is_valid():
            with transaction.atomic():
                passenger = passenger_serializer.save()
                ticket_data = ticket_serializer.validated_data
                ticket_data["passenger"] = passenger
                ticket_data["cart"] = cart
                ticket = Ticket.objects.create(**ticket_data)

                return Response(
                    {"message": "Ticket successfully created"}, status=201
                )

        return Response({"error": "Provided data not valid"}, status=400)

    def put(self, request: HttpRequest, ticket_pk: int) -> Response:
        try:
            ticket = get_ticket(ticket_pk)
        except ObjectDoesNotExist:
            return Response("Ticket does not exist", status=404)

        passenger = ticket.passenger
        ticket_serializer = TicketSerializer(
            data=request.data, instance=ticket
        )
        passenger_serializer = PassengerSerializer(
            data=request.data, instance=passenger
        )
        if passenger_serializer.is_valid() and ticket_serializer.is_valid():
            with transaction.atomic():
                ticket_serializer.save()
                passenger_serializer.save()

            return Response(
                {"message": "Ticket successfully updated"}, status=200
            )

        return Response({"Error": "Provided data not valid"}, status=400)
