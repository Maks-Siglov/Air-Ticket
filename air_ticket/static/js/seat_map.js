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
    })
    .catch(error => console.error(error));

function handleSeatSelection(event){
    const seat = event.currentTarget;
    const id = seat.dataset.id;

    console.log(`Selected seat id: ${id}`);
}


function createSeatElement(seat) {
    const seatElement = document.createElement('div');
    seatElement.dataset.id = seat.id;

    const imgElement = document.createElement('img');
    imgElement.width = 40;
    imgElement.src = seatImageUrl;
    imgElement.alt = 'Seat';

     if (!seat.is_available) {
        seatElement.classList.add('unavailable-seat', 'm-1');
    } else {
        seatElement.classList.add('seat', 'm-1');
        imgElement.classList.add('seat-image');
    }

    seatElement.appendChild(imgElement);

    return seatElement;
}
