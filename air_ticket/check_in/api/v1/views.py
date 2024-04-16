from django.db import IntegrityError, transaction

from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from orders.crud import (
    get_order_ticket_by_order,
    get_order_ticket_with_flight,
    get_order_with_flight
)


class SelectSeatView(APIView):
    def post(
        self, request: Request, seat_number: int, order_ticket_pk: int
    ) -> Response:
        if (
            order_ticket := get_order_ticket_with_flight(order_ticket_pk)
        ) is None:
            raise NotFound(detail=f"Ticket {order_ticket_pk} not found")
        flight = order_ticket.order.flight
        try:
            with transaction.atomic():
                order_ticket.seat_number = seat_number
                order_ticket.save()
                print(seat_number)
                flight.ordered_seats.append(seat_number)
                flight.save()
        except IntegrityError:
            return Response(
                {"error": "Try again later"}, status.HTTP_409_CONFLICT
            )
        return Response(status=200)


class DeclineSeatView(APIView):
    def post(
        self, request: Request, seat_number: int, order_pk: int
    ) -> Response:
        if (order := get_order_with_flight(order_pk)) is None:
            raise NotFound(detail=f"Order {order_pk} not found")

        if (
            order_ticket := get_order_ticket_by_order(order, seat_number)
        ) is None:
            raise NotFound(
                detail=f"Seat {seat_number} don't assigned to order's ticket"
            )

        flight = order.flight
        try:
            with transaction.atomic():
                order_ticket.seat_number = None
                order_ticket.save()
                flight.ordered_seats.remove(seat_number)
                flight.save()
        except IntegrityError:
            return Response(
                {"error": "Try again later"}, status.HTTP_409_CONFLICT
            )
        return Response(status=200)
