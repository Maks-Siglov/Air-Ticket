const seatSelectionCard = document.getElementById('seat-selection-card');
const selectSeatButton = document.getElementById('select-seat-button');

let selectedSeats = []

export function handleSeatSelection(event) {
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
    if (selectedSeats.length === 0) {
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
        console.log(ticketId)
        fetch(`/api/v1/check-in/select-seat/${seatId}/${ticketId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
            .then(response => {
                console.log(response)
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

function showSelectedSeats() {
    document.getElementById('selected-seat-id').textContent = selectedSeats;
    seatSelectionCard.classList.remove('d-none');
}

function updateSelectedSeatsCount() {
    document.getElementById('selected-seat-count').textContent = selectedSeats.length;
}

function getCookie(name) {
    const value = "; " + document.cookie;
    const parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}