const seatMapContainer = document.getElementById('seat-map-container');
const seatSelectionCard = document.getElementById('seat-selection-card');
const selectSeatButton = document.getElementById('select-seat-button');

const seatImageUrl = '/static/images/seat.png';

let selectedSeats = []

seatMapContainer.textContent = 'Loading seat map data...';

fetch('/api/v1/check-in/' + flightPk)
    .then(response => response.json())
    .then(seatsData => {
        seatMapContainer.textContent = '';

        const seatsAmount = seatsData.length;
        const rows = Math.floor(Math.sqrt(seatsAmount));
        const columns = 15

        for (let row = 0; row < rows; row++) {
            const rowElement = document.createElement('div');
            rowElement.classList.add(`seat-row-${row}`, 'd-flex', 'justify-content-center');

            for (let col = 0; col < columns; col++) {
                const seatIndex = row * columns + col;
                if (seatIndex < seatsData.length) {
                    const seat = seatsData[seatIndex];
                    const seatElement = createSeatElement(seat)

                    seatElement.addEventListener('click', handleSeatSelection);

                    rowElement.appendChild(seatElement);
                }
            }

    seatMapContainer.appendChild(rowElement);
}
    })
    .catch(error => console.error(error));

function handleSeatSelection(event) {
    if (selectedSeats.length >= 4) {
        console.warn("Maximum seat selection reached (4)");
        return;
    }

    const seat = event.currentTarget;
    const seatId = seat.dataset.id;

    if (selectedSeats.includes(seatId)) {
        removeSelectedSeat(seat, seatId);
    } else {
        addSelectedSeat(seat, seatId);
    }
}

function removeSelectedSeat(seat, seatId) {
    const seatIndex = selectedSeats.indexOf(seatId);
    selectedSeats.splice(seatIndex, 1);

    const seatElement = document.querySelector(`.seat-${seatId}`);
    const seatImg = seatElement.querySelector('img');
    seatImg.style.backgroundColor = '';

    seat.classList.remove('selected');
    seat.disabled = false;

    updateSelectedSeatsCount();
}

function addSelectedSeat(seat, seatId) {
    selectedSeats.push(seatId);

    const seatElement = document.querySelector(`.seat-${seatId}`);
    const seatImg = seatElement.querySelector('img');
    seatImg.style.backgroundColor = 'green';

    updateSelectedSeatsCount();

    selectSeat(seat, seatId);
}

function selectSeat(seat, seatId) {
    document.getElementById('selected-seat-id').textContent = selectedSeats;
    seatSelectionCard.classList.remove('d-none');

    selectSeatButton.addEventListener('click', function () {
        fetch('/api/v1/check-in/select-seat/', {
            method: 'POST',
            body: JSON.stringify({ seatId: seatId }),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (response.ok) {
                seat.classList.add('unavailable');
            } else {
                console.error('Error selecting seat:', response.statusText);
            }
        })
        .catch(error => console.error('Error:', error));

        selectSeatButton.removeEventListener('click', this);
    });
}

function updateSelectedSeatsCount() {
    document.getElementById('selected-seat-count').textContent = `Selected seats: ${selectedSeats.length}`;
}


function createSeatElement(seat) {
    const seatElement = document.createElement('div');
    const seatId = seat.id
    seatElement.dataset.id = seatId

    const imgElement = document.createElement('img');
    imgElement.width = 40;
    imgElement.src = seatImageUrl;
    imgElement.alt = 'Seat';

     if (!seat.is_available) {
        seatElement.classList.add('unavailable-seat', 'm-1');
    } else {
        seatElement.classList.add(`seat-${seatId}`, 'm-1');
        imgElement.classList.add('seat-image');
    }

    seatElement.appendChild(imgElement);

    return seatElement;
}

function getCookie(name) {
    const value = "; " + document.cookie;
    const parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}