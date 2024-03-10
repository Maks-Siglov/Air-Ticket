const rows = Math.floor(Math.sqrt(seatsCount));
const columns = Math.ceil(seatsCount / rows);

const corridorRow = 3
const seatAvailability = [];
const seatImageUrl = '/static/images/seat.png'

for (let row = 0; row < rows ; row++) {
    seatAvailability.push([]);
    for (let col = 0; col < columns; col++) {
        seatAvailability[row].push(true);
    }
}

function generateSeatMap() {
    const seatMapContainer = document.getElementById('seat-map-container');
    seatMapContainer.innerHTML = '';

    for (let row = 1; row < rows + 1; row++){
        const rowElement = document.createElement('div')
        rowElement.classList.add(`seat-row-${row}`, 'm-1')

        if (row === corridorRow){
            rowElement.classList.add('mb-4')
        }

        for (let col = 1; col < columns + 1 ; col++){
            const seatElement = createSeatElement(row, col)

            createSeatImgElement(seatElement)

            if (!seatAvailability[row - 1][col - 1]) {
                seatElement.classList.add('unavailable');
            }

            seatElement.addEventListener('click', handleSeatSelection);

            rowElement.appendChild(seatElement);
        }
        seatMapContainer.appendChild(rowElement)
    }
}

function handleSeatSelection(event){
    const seat = event.currentTarget;
    const row = seat.dataset.row;
    const column = seat.dataset.column;

    console.log(`Seat selected: Row ${row}, Column ${column}`);
}

function createSeatElement(row, col){
    const seatElement = document.createElement('span');
    seatElement.classList.add('seat', 'm-2');
    seatElement.dataset.row = row;
    seatElement.dataset.column = col;
    return seatElement
}

function createSeatImgElement(seatElement){
    const imgElement = document.createElement('img');
    imgElement.width = 40
    imgElement.src = seatImageUrl;
    imgElement.alt = 'Seat';
    imgElement.classList.add('seat-image')
    seatElement.appendChild(imgElement);
}

generateSeatMap();
