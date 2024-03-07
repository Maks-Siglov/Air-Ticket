import pytest

from flight.models import Airplane, Airport, Flight
from users.models import User


@pytest.fixture
def test_flight(db) -> User:
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

    test_airplane = Airplane.objects.create(name="Cirrus King Air-4660")

    test_flight = Flight.objects.create(
        departure_airport=test_departure_airport,
        arrival_airport=test_arrival_airport,
        airplane=test_airplane,
        departure_scheduled="2024-03-03 17:05:00.000000 +00:00",
        arrival_scheduled="2024-03-03 19:55:00.000000 +00:00",
        iata="MH9906",
        icao="MAS9906",
    )

    yield test_flight

    test_airplane.delete()
    test_arrival_airport.delete()
    test_departure_airport.delete()
    test_flight.delete()
