let rows = 6;
let columns = 10;
let corridorRow = 4
const seatAvailability = [];
const seatImageUrl = '/static/images/seat.png'


function generateSeatMap() {
    const seatMapContainer = document.getElementById('seat-map-container');
    seatMapContainer.innerHTML = '';

    for (let row = 1; row < rows + 1; row++){
        const rowElement = document.createElement('div')
        rowElement.classList.add(`seat-row-${row}`, 'm-1')

        if (row === corridorRow){
            appendCorridorRow(seatMapContainer)
        }

        for (let col = 1; col < columns + 1 ; col++){
            const seatElement = document.createElement('span');
            seatElement.classList.add('seat', 'm-2');
            seatElement.dataset.row = row;
            seatElement.dataset.column = col;

            const imgElement = document.createElement('img');
            imgElement.width = 40
            imgElement.src = seatImageUrl;
            imgElement.alt = 'Seat';
            seatElement.appendChild(imgElement);

            rowElement.appendChild(seatElement);
        }
        seatMapContainer.appendChild(rowElement)
    }
}

function appendCorridorRow(seatMap){
    const corridorRow = document.createElement('div');
    corridorRow.classList.add('corridor-row', 'm-4');
    seatMap.appendChild(corridorRow);
}

generateSeatMap();