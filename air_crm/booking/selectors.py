from flight.models import Airplane, Seat


def get_seat(airplane: Airplane, seat_type: str) -> Seat:
    seat = Seat.objects.filter(
        airplane=airplane, type=seat_type.capitalize(), is_available=True
    ).first()
    print(seat)
    seat.is_available = False
    seat.save()
    return seat
