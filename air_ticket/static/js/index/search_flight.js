const formContainer = document.getElementById('container-search-form')
const searchForm = document.getElementById('search-form')
const flightsContainer = document.getElementById('flights-container');

searchForm.addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch('/api/v1/flights/search-flights/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        formContainer.style.display = 'none';
        displayFlights(data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
});


function displayFlights(data) {
    flightsContainer.innerHTML = '';

    const flights = data.flights;
    const flightsCount = data.flights_count;
    const passengerAmount = data.passenger_amount;
    const arrivalCity = data.arrival_city;
    const departureCity = data.departure_city;
    const departureDate = data.departure_date;

    if (flights.length > 0) {
        const h2 = document.createElement('h2');
        h2.textContent = `${passengerAmount} passenger${passengerAmount > 1 ? 's' : ''} From ${departureCity} to ${arrivalCity} in ${departureDate}`;
        flightsContainer.appendChild(h2);

        const br = document.createElement('br');
        flightsContainer.appendChild(br);

        const h4 = document.createElement('h4');
        h4.textContent = `${flightsCount} Flights Found`;
        flightsContainer.appendChild(h4);

        const hr = document.createElement('hr');
        flightsContainer.appendChild(hr);

        flights.forEach(flight => {
            const card = document.createElement('div');
            card.classList.add('card', 'mb-3');

            const cardHeader = document.createElement('div');
            cardHeader.classList.add('card-header', 'd-flex', 'justify-content-between', 'align-items-center');

            const cardTitle = document.createElement('h5');
            cardTitle.classList.add('card-title');
            cardTitle.textContent = `${flight.departure_airport__name} to ${flight.arrival_airport__name}`;
            cardHeader.appendChild(cardTitle);

            const cardInfo = document.createElement('div');
            const cardInfoP1 = document.createElement('p');
            cardInfoP1.classList.add('m-0');
            cardInfoP1.textContent = `${flight.airplane_total_seats} Seats:`;
            const cardInfoP2 = document.createElement('p');
            cardInfoP2.classList.add('m-0');
            cardInfoP2.textContent = `Economy: ${flight.airplane_economy_seats} Business: ${flight.airplane_business_seats} First class: ${flight.airplane_first_class_seats}`;
            cardInfo.appendChild(cardInfoP1);
            cardInfo.appendChild(cardInfoP2);

            cardHeader.appendChild(cardInfo);
            card.appendChild(cardHeader);

            const cardBody = document.createElement('div');
            cardBody.classList.add('card-body', 'd-flex', 'justify-content-between', 'align-items-center');

            const cardText = document.createElement('div');
            const cardTextP1 = document.createElement('p');
            cardTextP1.classList.add('card-text');
            cardTextP1.textContent = `Airplane: ${flight.airplane__name}`;
            const cardTextP2 = document.createElement('p');
            cardTextP2.classList.add('card-text');
            cardTextP2.textContent = `Departure Date: ${flight.departure_scheduled} T/Z: ${flight.departure_airport__timezone}`;
            const cardTextP3 = document.createElement('p');
            cardTextP3.classList.add('card-text');
            cardTextP3.textContent = `Arrival Date: ${flight.arrival_scheduled} T/Z: ${flight.arrival_airport__timezone}`;
            cardText.appendChild(cardTextP1);
            cardText.appendChild(cardTextP2);
            cardText.appendChild(cardTextP3);

            cardBody.appendChild(cardText);

            const cardDiv = document.createElement('div');
            cardDiv.classList.add('ml-auto');

            const cardLink = document.createElement('a');
            cardLink.classList.add('btn', 'btn-primary');
            cardLink.href = `/booking/create_order/${flight.id}?passenger_amount=${passengerAmount}`;
            cardLink.textContent = 'Book Now';

            cardDiv.appendChild(cardLink);
            cardBody.appendChild(cardDiv);

            card.appendChild(cardBody);
            flightsContainer.appendChild(card);
        });
    } else {
        const noFlightsText = document.createElement('p');
        noFlightsText.textContent = 'No flights found.';
        flightsContainer.appendChild(noFlightsText);
    }
}
