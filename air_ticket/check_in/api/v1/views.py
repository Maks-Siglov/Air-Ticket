from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest

from rest_framework.response import Response
from rest_framework.views import APIView

from check_in.api.v1.serializers import SeatSerializer
from flight.models import Seat, Flight
from orders.models import OrderTicket


class SeatsView(APIView):
    def get(self, request: HttpRequest, flight_pk: int) -> Response:
        flight = Flight.objects.select_related("airplane").get(pk=flight_pk)
        seats = Seat.objects.all().order_by("id")[
            : flight.airplane.seats_amount
        ]
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)


class SelectSeatView(APIView):
    def post(self, request: HttpRequest, seat_pk: int) -> Response:
        order_ticket_pk = request.data["ticketId"]
        try:
            order_ticket = OrderTicket.objects.get(pk=order_ticket_pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": f"Ticket with id {order_ticket_pk} not found"},
                status=404,
            )
        try:
            seat = Seat.objects.get(pk=seat_pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": f"Seat with id {seat_pk} not found"}, status=404
            )

        order_ticket.seat = seat
        order_ticket.save()
        return Response(status=200)


class DeclineSeatView(APIView):
    def post(self, request: HttpRequest, seat_pk: int) -> Response:
        try:
            seat = Seat.objects.get(pk=seat_pk)
        except ObjectDoesNotExist:
            return Response(
                {"error": f"Seat with id {seat_pk} not found"}, status=404
            )
        try:
            order_ticket = OrderTicket.objects.get(seat=seat)
        except ObjectDoesNotExist:
            return Response(
                {"error": f"Seat {seat_pk} don't assigned to order's ticket"},
                status=404,
            )
        order_ticket.seat = None
        order_ticket.save()
        seat.is_available = True
        seat.save()
        return Response(status=200)
