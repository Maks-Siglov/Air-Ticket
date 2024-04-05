from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpRequest
from rest_framework.response import Response
from rest_framework.views import APIView

from check_in.api.v1.serializers import SeatSerializer
from flight.models import Seat
from flight.selectors import get_airplane_seats, get_flight_with_airplane
from orders.selectors import get_order_ticket, get_order_ticket_by_seat


class SeatsView(APIView):
    def get(self, request: HttpRequest, flight_pk: int) -> Response:
        try:
            flight = get_flight_with_airplane(flight_pk)
        except ObjectDoesNotExist:
            return Response("Flight does not exist", status=404)

        seats = get_airplane_seats(flight.airplane)
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)


class SelectSeatView(APIView):
    def post(self, request: HttpRequest, seat_pk: int) -> Response:
        order_ticket_pk = request.data["ticketId"]
        try:
            order_ticket = get_order_ticket(order_ticket_pk)
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
            order_ticket = get_order_ticket_by_seat(seat)
        except ObjectDoesNotExist:
            return Response(
                {"error": f"Seat {seat_pk} don't assigned to order's ticket"},
                status=404,
            )
        order_ticket.seat = None
        order_ticket.save()
        return Response(status=200)
