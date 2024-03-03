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
