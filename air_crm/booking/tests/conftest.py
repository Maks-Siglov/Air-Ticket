import pytest

from booking.models import TicketCart, Ticket
from customer.models import Contact, Passenger
from flight.models import Airport, Flight, Airplane, Seat


@pytest.fixture
def test_airplane_with_seats(db):
    test_airplane = Airplane.objects.create(name="Cirrus King Air-4660")
    economy_seat = Seat.objects.create(type="Economy", airplane=test_airplane)
    business_seat = Seat.objects.create(
        type="Business", airplane=test_airplane
    )

    yield test_airplane

    economy_seat.delete()
    business_seat.delete()
    test_airplane.delete()


@pytest.fixture
def test_flight(db, test_airplane_with_seats: Airplane) -> Flight:
    test_departure_airport = Airport.objects.create(
        name="Vienna International",
        timezone="Europe/Vienna",
        iata="VIE",
        icao="LOWW",
    )
    test_arrival_airport = Airport.objects.create(
        name="Berlin Brandenburg Airport",
        timezone="Europe/Berlin",
        iata="BER",
        icao="EDDB",
    )

    test_flight = Flight.objects.create(
        departure_airport=test_departure_airport,
        arrival_airport=test_arrival_airport,
        airplane=test_airplane_with_seats,
        departure_scheduled="2024-03-03 17:05:00.000000 +00:00",
        arrival_scheduled="2024-03-03 19:55:00.000000 +00:00",
        iata="MH9906",
        icao="MAS9906",
    )

    yield test_flight

    test_departure_airport.delete()
    test_arrival_airport.delete()
    test_flight.delete()


@pytest.fixture
def test_cart(db, test_flight: Flight) -> TicketCart:
    cart = TicketCart.objects.create(flight=test_flight, passenger_amount=2)

    yield cart


@pytest.fixture
def test_contact(db) -> Contact:
    contact = Contact.objects.create(
        phone_number="0673335623", email="test@gmail.com"
    )

    yield contact

    contact.delete()


@pytest.fixture
def test_ticket(db, test_cart: TicketCart) -> Ticket:

    passenger = Passenger.objects.create(
        first_name="test_first_name",
        last_name="test_last_name",
        passport_id="331542159",
    )

    seat = Seat.objects.filter(airplane=test_cart.flight.airplane).first()

    ticket = Ticket.objects.create(
        cart=test_cart,
        passenger=passenger,
        seat=seat,
        price=200,
        lunch=False,
        luggage=False,
    )

    yield ticket

    passenger.delete()
    ticket.delete()
