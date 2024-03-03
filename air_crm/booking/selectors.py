from flight.models import Airplane, Seat


def get_seat(airplane: Airplane, seat_type: str) -> Seat:
    seat = Seat.objects.filter(
        airplane=airplane, type=seat_type.capitalize()
    ).first()

    return seat
