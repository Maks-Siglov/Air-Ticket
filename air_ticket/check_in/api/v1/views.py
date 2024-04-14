from django.http import HttpRequest

from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from check_in.api.v1.serializers import SeatSerializer
from flight.crud import get_airplane_seats, get_flight_with_airplane
from flight.models import Seat
from orders.crud import get_order_ticket, get_order_ticket_by_seat


class SeatsView(APIView):
    def get(self, request: HttpRequest, flight_pk: int) -> Response:
        if (flight := get_flight_with_airplane(flight_pk)) is None:
            raise NotFound("Flight not found")
        seats = get_airplane_seats(flight.airplane)
        serializer = SeatSerializer(seats, many=True)
        return Response(serializer.data)


class SelectSeatView(APIView):
    def post(self, request: HttpRequest, seat_pk: int) -> Response:
        order_ticket_pk = request.data["ticketId"]
        if (order_ticket := get_order_ticket(order_ticket_pk)) is None:
            raise NotFound(detail=f"Ticket {order_ticket_pk} not found")
        if (seat := Seat.objects.filter(pk=seat_pk).first) is None:
            raise NotFound(detail=f"Seat with id {seat_pk} not found")

        order_ticket.seat = seat
        order_ticket.save()
        return Response(status=200)


class DeclineSeatView(APIView):
    def post(self, request: HttpRequest, seat_pk: int) -> Response:
        if (seat := Seat.objects.filter(pk=seat_pk).first) is None:
            raise NotFound(detail=f"Seat with id {seat_pk} not found")
        if (order_ticket := get_order_ticket_by_seat(seat)) is None:
            raise NotFound(
                detail=f"Seat {seat_pk} don't assigned to order's ticket"
            )
        order_ticket.seat = None
        order_ticket.save()
        return Response(status=200)
