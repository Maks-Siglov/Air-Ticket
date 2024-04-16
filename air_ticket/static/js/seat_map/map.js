import {handleSeatSelection} from './select_seat.js';
import {handleCancelSeat} from "./cancel_seat.js";

const seatMapContainer = document.getElementById('seat-map-container');
const seatImageUrl = '/static/images/seat.png';

const seatsPerPage = 80;
let currentPage = 1;


function generateSeatMap() {
    seatMapContainer.innerHTML = '';
    console.log(seatMapContainer.innerHTML)

    const seatsData = allSeats
    const seatsAmount = seatsData.length;

    const totalPages = Math.ceil(seatsAmount / seatsPerPage);

    const startIndex = (currentPage - 1) * seatsPerPage;
    const endIndex = Math.min(startIndex + seatsPerPage, seatsAmount);

    const rows = 4;
    const columns = Math.ceil(seatsPerPage / rows);

    for (let row = 0; row < rows; row++) {
        const rowElement = createRowElement(row)

        for (let col = 0; col < columns; col++) {
            const seatIndex = row * columns + col + startIndex;
            if (seatIndex < endIndex) {
                const seatId = seatsData[seatIndex];

                const seatElement = createSeatElement(seatId)

                seatElement.addEventListener('click', handleSeatSelection);

                rowElement.appendChild(seatElement);
            }
        }

        seatMapContainer.appendChild(rowElement);
    }
    displaySelectedSeats();
    displaySelectedUserSeat();

    generatePagination(currentPage, totalPages);
}

function generatePagination(currentPage, totalPages){
    const paginationContainer = document.getElementById('pagination-container');
    paginationContainer.innerHTML = '';

    const previousButton = document.createElement('button');
    previousButton.id = 'previous-page-btn';
    previousButton.className = 'btn btn-secondary mx-2';
    previousButton.textContent = 'Previous';
    previousButton.addEventListener('click', () => previousPage());

    const currentPageSpan = document.createElement('span');
    currentPageSpan.id = 'current-page';
    currentPageSpan.textContent = `Page ${currentPage} of ${totalPages}`;

    const nextButton = document.createElement('button');
    nextButton.id = 'next-page-btn';
    nextButton.className = 'btn btn-secondary mx-2';
    nextButton.textContent = 'Next';
    nextButton.addEventListener('click', () => nextPage(totalPages));

    paginationContainer.appendChild(previousButton);
    paginationContainer.appendChild(currentPageSpan);
    paginationContainer.appendChild(nextButton);
}

function nextPage(totalPages) {
    if (currentPage < totalPages) {
        currentPage++;
        generateSeatMap();
    }
}

function previousPage() {
    if (currentPage > 1) {
        currentPage--;
        generateSeatMap();
    }
}

function createSeatElement(seatId) {
    const seatElement = document.createElement('div');
    seatElement.dataset.id = seatId

    const imgElement = document.createElement('img');
    imgElement.width = 40;
    imgElement.src = seatImageUrl;
    imgElement.alt = 'Seat';

    seatElement.classList.add(`seat-${seatId}`, 'm-1');
    imgElement.classList.add('seat-image');

    seatElement.appendChild(imgElement);

    return seatElement;
}

function createRowElement(row){
    const rowElement = document.createElement('div');
    rowElement.classList.add(`seat-row-${row}`, 'd-flex', 'justify-content-center');
    return rowElement
}

function displaySelectedSeats() {
     if (orderedSeats.length) {
        orderedSeats.forEach(seatId => {
            const seatElement = document.querySelector(`.seat-${seatId}`);
            if (seatElement) {
                seatElement.classList.add('unavailable', `seat-${seatId}`, 'm-1');
                const imgElement = seatElement.querySelector('img')
                imgElement.classList.remove('seat-image');
                seatElement.removeEventListener('click', handleSeatSelection)
            }
        });
    }
}

function displaySelectedUserSeat() {
    if (userSeatIds.length) {
        userSeatIds.forEach(seatId => {
            const seatElement = document.querySelector(`.seat-${seatId}`);
            if (seatElement) {
                seatElement.classList.remove('unavailable')
                seatElement.classList.add('selected')
                seatElement.addEventListener('click', handleCancelSeat)
            }
        });
    }
}

generateSeatMap();
document.getElementById('previous-page-btn').addEventListener('click', previousPage);
document.getElementById('next-page-btn').addEventListener('click', nextPage);