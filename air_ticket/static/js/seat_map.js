const seatMapContainer = document.getElementById('seat-map-container');
const seatSelectionCard = document.getElementById('seat-selection-card');
const selectSeatButton = document.getElementById('select-seat-button');
const seatDeclineSelectionCard = document.getElementById('seat-decline-card')
const declineSeatButton = document.getElementById('decline-seat-button')

const seatImageUrl = '/static/images/seat.png';

let declinedSeats = []
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
        displaySelectedUserSeat();
    })
    .catch(error => console.error(error));

function handleSeatSelection(event) {
    const seat = event.currentTarget;
    const seatId = seat.dataset.id;

    if (selectedSeats.includes(seatId)) {
        removeSelectedSeat(seat, seatId);
        return;
    }
    if (selectedSeats.length >= ticketsAmount) {
        console.warn(`Maximum seat selection reached (${ticketsAmount})`);
        return;
    }

    addSelectedSeat(seat, seatId);

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
    if (selectedSeats.length === 0){
         seatSelectionCard.classList.add('d-none');
    } else {
        showSelectedSeats();
    }
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
    showSelectedSeats();

    selectSeatButton.addEventListener('click', function () {
        const ticketId = getFirstTicketId();
        fetch('/api/v1/check-in/select-seat/' + seatId, {
            method: 'POST',
            body: JSON.stringify({ticketId: ticketId}),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                console.error('Error selecting seat:', response.statusText);
            }
        })
        .catch(error => console.error('Error:', error));

        selectSeatButton.removeEventListener('click', this);
    });
}

function getFirstTicketId() {
  if (!ticketIDs.length) {
    throw new Error('No ticket IDs available for selection.');
  }
  return ticketIDs.shift();
}

function showSelectedSeats(){
    document.getElementById('selected-seat-id').textContent = selectedSeats;
    seatSelectionCard.classList.remove('d-none');
}

function updateSelectedSeatsCount() {
    document.getElementById('selected-seat-count').textContent = selectedSeats.length;
}


function displaySelectedUserSeat() {
    if (approvedSelectedSeatsIDs.length) {
        approvedSelectedSeatsIDs.forEach(seatId => {
            const seatElement = document.querySelector(`.seat-${seatId}`);
            if (seatElement) {
                seatElement.classList.remove('unavailable')
                seatElement.classList.add('selected')
                seatElement.removeEventListener('click', handleSeatSelection)
                seatElement.addEventListener('click', handleDeclineSeatSelection)
            }
        });
    }
}


function handleDeclineSeatSelection(event) {
    const seat = event.currentTarget;
    const seatId = seat.dataset.id;

    if (declinedSeats.includes(seatId)) {
        removeDeclineSelectedSeat(seat, seatId);
        return;
    }

    declineSelectedSeat(seat, seatId);

    showDeclineSelectedSeats();
}


function declineSelectedSeat(seat, seatID){
    declinedSeats.push(seatID)

    seat.classList.remove('selected');
    seat.classList.add('declined')

    declineSeat(seat, seatID)
}

function removeDeclineSelectedSeat(seat, seatID){
    const seatIndex = declinedSeats.indexOf(seatID);
    declinedSeats.splice(seatIndex, 1);

    seat.classList.remove('declined');
    seat.classList.add('selected')

    if (declinedSeats.length === 0){
        seatDeclineSelectionCard.classList.add('d-none');
    } else {
        showDeclineSelectedSeats();
    }
}


function declineSeat(seat, seatID){
    showDeclineSelectedSeats()

    declineSeatButton.addEventListener('click', function () {
        fetch('/api/v1/check-in/decline-seat/' + seatID, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (response.ok) {
                window.location.reload();
            } else {
                console.error('Error selecting seat:', response.statusText);
            }
        })
        .catch(error => console.error('Error:', error));

        declineSeatButton.removeEventListener('click', this);
    });
}

function showDeclineSelectedSeats(){
    document.getElementById('decline-seat-id').textContent = declinedSeats;
    seatDeclineSelectionCard.classList.remove('d-none');
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
        seatElement.classList.add('unavailable', `seat-${seatId}`, 'm-1');
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