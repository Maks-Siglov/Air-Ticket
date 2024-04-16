const seatDeclineSelectionCard = document.getElementById('seat-decline-card');
const declineSeatButton = document.getElementById('decline-seat-button');

let canceledSeatId = null;

export function handleCancelSeat(event) {
    const seat = event.currentTarget;
    const seatId = seat.dataset.id;

    if (canceledSeatId === seatId) {
        removeCancelSeat(seat);
        canceledSeatId = null;
        return;
    }
    if (canceledSeatId){
        removePreviousCancelSeat();
        canceledSeatId = null;
    }

    canceledSeatId = seatId;
    cancelSeat(seat, seatId);
    showCancelSeats();
}

function cancelSeat(seat, seatId) {
    canceledSeatId = seatId;

    seat.classList.remove('selected');
    seat.classList.add('declined');

    declineSeat();
}

function removeCancelSeat(seat) {
    const seatElement = document.querySelector(`.seat-${canceledSeatId}`);

    seat.classList.remove('declined');
    seat.classList.add('selected');
    
    seatDeclineSelectionCard.classList.add('d-none');

}

function removePreviousCancelSeat(){
    const seatElement = document.querySelector(`.seat-${canceledSeatId}`);

    seatElement.classList.remove('declined');
    seatElement.classList.add('selected');

    seatDeclineSelectionCard.classList.add('d-none');
}

function declineSeat() {
    showCancelSeats();

    declineSeatButton.addEventListener('click', function () {
        if (canceledSeatId) {
            fetch(`/api/v1/check-in/decline-seat/${canceledSeatId}/order/${orderId}`, {
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

            canceledSeatId = null;
            declineSeatButton.removeEventListener('click', this);
        }
    });
}

function showCancelSeats() {
    document.getElementById('decline-seat-id').textContent = canceledSeatId;
    seatDeclineSelectionCard.classList.remove('d-none');
}

function getCookie(name) {
    const value = "; " + document.cookie;
    const parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}
