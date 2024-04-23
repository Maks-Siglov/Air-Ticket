import pytest
from booking.models import (
    Booking,
    Ticket,
    TicketCart
)
from customer.models import Contact, Passenger
from flight.models import (
    Airplane,
    Airport,
    Flight
)


@pytest.fixture
def test_airplane(db):
    test_airplane = Airplane.objects.create(
        name="Cirrus King Air-4660", seats_amount=20
    )

    yield test_airplane


@pytest.fixture
def test_flight(db, test_airplane: Airplane) -> Flight:
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
        airplane=test_airplane,
        departure_scheduled="2024-03-03 17:05:00.000000 +00:00",
        arrival_scheduled="2024-03-03 19:55:00.000000 +00:00",
        iata="MH9906",
        icao="MAS9906",
        seats=[1, 2, 10, 11],
        booked_seats=[10, 11],
    )
    yield test_flight


@pytest.fixture
def test_contact(db) -> Contact:
    contact = Contact.objects.create(
        phone_number="0673335623", email="test@gmail.com"
    )

    yield contact


@pytest.fixture
def test_cart(db, test_flight: Flight, test_contact: Contact) -> TicketCart:
    cart = TicketCart.objects.create(
        flight=test_flight, passenger_amount=1, contact=test_contact
    )
    passenger = Passenger.objects.create(
        first_name="test_first_name",
        last_name="test_last_name",
        passport_id="331542159",
    )
    Ticket.objects.create(
        cart=cart,
        passenger=passenger,
        flight=test_flight,
        price=200,
        lunch=False,
        luggage=False,
    )

    Booking.objects.create(flight=test_flight, cart=cart, booked_seat_number=1)

    yield cart


@pytest.fixture
def test_empty_cart(db, test_flight: Flight):
    cart = TicketCart.objects.create(flight=test_flight, passenger_amount=1)
    Booking.objects.create(flight=test_flight, cart=cart, booked_seat_number=1)

    yield cart


@pytest.fixture
def test_bookings(db, test_flight):
    cart = TicketCart.objects.create(flight=test_flight, passenger_amount=1)
    Booking.objects.create(
        flight=test_flight, cart=cart, booked_seat_number=10
    )
    Booking.objects.create(
        flight=test_flight, cart=cart, booked_seat_number=11
    )

    yield
