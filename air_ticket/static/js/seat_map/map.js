import {handleSeatSelection} from './select_seat.js';
import {handleCancelSeat} from "./cancel_seat.js";

const seatMapContainer = document.getElementById('seat-map-container');

const seatImageUrl = '/static/images/seat.png';
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
        displaySelectedUserSeat();
    })
    .catch(error => console.error(error));

function createSeatElement(seat) {
    const seatElement = document.createElement('div');
    const seatId = seat.id
    seatElement.dataset.id = seatId

    const imgElement = document.createElement('img');
    imgElement.width = 40;
    imgElement.src = seatImageUrl;
    imgElement.alt = 'Seat';

    if (!seat.is_available) {
        seatElement.classList.add('unavailable', `seat-${seatId}`, 'm-1');
    } else {
        seatElement.classList.add(`seat-${seatId}`, 'm-1');
        imgElement.classList.add('seat-image');
    }

    seatElement.appendChild(imgElement);

    return seatElement;
}

function displaySelectedUserSeat() {
    if (approvedSelectedSeatsIDs.length) {
        approvedSelectedSeatsIDs.forEach(seatId => {
            const seatElement = document.querySelector(`.seat-${seatId}`);
            if (seatElement) {
                seatElement.classList.remove('unavailable')
                seatElement.classList.add('selected')
                seatElement.removeEventListener('click', handleSeatSelection)
                seatElement.addEventListener('click', handleCancelSeat)
            }
        });
    }
}
