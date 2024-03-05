document.addEventListener('DOMContentLoaded', function() {
    const formTicket = document.getElementById('ticketForm')
    formTicket.addEventListener('submit', function(event) {
        event.preventDefault()

        const formData = new FormData(this)

        const xhr = new XMLHttpRequest();
        xhr.open('POST', formTicket.action);
        xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
        xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        xhr.onload = function() {
            console.log(xhr.status)
            if (xhr.status === 201) {

                const response = JSON.parse(xhr.responseText);
                console.log(response)
                console.log(xhr.response)
                displayTicketDetails(xhr.response);

            } else {
                console.error(xhr.responseText);
            }
        }
         xhr.send(formData);
    })
})


function getCookie(name) {
    const value = "; " + document.cookie;
    const parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}


function displayTicketDetails(response) {
    const data = JSON.parse(response);

    const ticketCard = document.createElement('div');
    ticketCard.classList.add('card', 'mb-1');

    const cardHeader = document.createElement('div');
    cardHeader.classList.add('card-header');
    cardHeader.textContent = `Ticket Details`;
    ticketCard.appendChild(cardHeader);

    const cardBody = document.createElement('div');
    cardBody.classList.add('card-body', 'text-center');

    const passengerDetails = document.createElement('p');
    passengerDetails.textContent = `Passenger: ${data.first_name} ${data.last_name}`;
    cardBody.appendChild(passengerDetails);

    const ticketDetails = document.createElement('p');
    ticketDetails.textContent = `Price: ${data.ticket_price}`;
    cardBody.appendChild(ticketDetails);

    ticketCard.appendChild(cardBody);

    const existingCardBody = document.getElementById('checkout-card-body');
    existingCardBody.appendChild(ticketCard);
}