const seatSelectionCard = document.getElementById('seat-selection-card');
const selectSeatButton = document.getElementById('select-seat-button');

let selectedSeatId = null;

export function handleSeatSelection(event) {
    const seat = event.currentTarget;
    const seatId = seat.dataset.id;

    if (selectedSeatId === seatId) {
        removeSelectedSeat(seatId);
        selectedSeatId = null;
        return;
    }
    if (selectedSeatId) {
        removeSelectedSeat(selectedSeatId);
        selectedSeatId = null
    }

    selectedSeatId = seatId;
    addSelectedSeat(seat, seatId);
}

function removeSelectedSeat(seatId) {
    const seatElement = document.querySelector(`.seat-${seatId}`);
    const seatImg = seatElement.querySelector('img');
    seatImg.style.backgroundColor = '';

    seatElement.classList.remove('selected');
    seatElement.disabled = false;

    updateSelectedSeatsCount();
    if (selectedSeatId === null) {
        seatSelectionCard.classList.add('d-none');
    } else {
        showSelectedSeats();
    }
}

function addSelectedSeat(seat, seatId) {
    const seatElement = document.querySelector(`.seat-${seatId}`);
    const seatImg = seatElement.querySelector('img');
    seatImg.style.backgroundColor = 'green';

    updateSelectedSeatsCount();

    selectSeat();
}

function selectSeat() {
    showSelectedSeats();

    selectSeatButton.addEventListener('click', function () {
        if (selectedSeatId) {
            const ticketId = getFirstTicketId();
            fetch(`/api/v1/check-in/select-seat/${selectedSeatId}/ticket/${ticketId}`, {
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

            selectedSeatId = null;
            selectSeatButton.removeEventListener('click', this);
        }
    });

}

function getFirstTicketId() {
    if (!ticketIDs.length) {
        throw new Error('No ticket IDs available for selection.');
    }
    return ticketIDs.shift();
}

function showSelectedSeats() {
    document.getElementById('selected-seat-id').textContent = selectedSeatId;
    seatSelectionCard.classList.remove('d-none');
}

function updateSelectedSeatsCount() {
    document.getElementById('selected-seat-count').textContent = 1;
}

function getCookie(name) {
    const value = "; " + document.cookie;
    const parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}