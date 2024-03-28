const seatDeclineSelectionCard = document.getElementById('seat-decline-card')
const declineSeatButton = document.getElementById('decline-seat-button')

let canceledSeats = []


export function handleCancelSeat(event) {
    const seat = event.currentTarget;
    const seatId = seat.dataset.id;

    if (canceledSeats.includes(seatId)) {
        removeCancelSeat(seat, seatId);
        return;
    }

    cancelSeat(seat, seatId);

    showCancelSeats();
}

function cancelSeat(seat, seatID) {
    canceledSeats.push(seatID)

    seat.classList.remove('selected');
    seat.classList.add('declined')

    declineSeat(seat, seatID)
}

function removeCancelSeat(seat, seatID) {
    const seatIndex = canceledSeats.indexOf(seatID);
    canceledSeats.splice(seatIndex, 1);

    seat.classList.remove('declined');
    seat.classList.add('selected')

    if (canceledSeats.length === 0) {
        seatDeclineSelectionCard.classList.add('d-none');
    } else {
        showCancelSeats();
    }
}

function declineSeat(seat, seatID) {
    showCancelSeats()

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

function showCancelSeats() {
    document.getElementById('decline-seat-id').textContent = canceledSeats;
    seatDeclineSelectionCard.classList.remove('d-none');
}

function getCookie(name) {
    const value = "; " + document.cookie;
    const parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}