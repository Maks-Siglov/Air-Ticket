document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form#ticketForm, form#contactForm');

    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const methodInput = form.querySelector('input[name="_method"]');
            const method = methodInput ? methodInput.value : 'POST';

            const formData = new FormData(this);

            const xhr = new XMLHttpRequest();
            xhr.open(method, form.action);
            xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
            xhr.onload = function() {
                if (xhr.status === 201 || xhr.status === 200) {
                    location.reload();
                } else {
                    const response = JSON.parse(xhr.responseText);
                    const errorMessage = response.error;

                    let errorDiv = form.querySelector('.alert-danger');
                    if (!errorDiv) {
                        errorDiv = document.createElement('div');
                        errorDiv.classList.add('alert', 'alert-danger');
                        form.insertBefore(errorDiv, form.firstChild);
                    }
                    errorDiv.textContent = errorMessage;
                }
            };
            xhr.send(formData);
        });
    });
});

function getCookie(name) {
    const value = "; " + document.cookie;
    const parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}
