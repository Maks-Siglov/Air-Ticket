function handleInputSuggestions(inputElement, suggestionElement) {
    inputElement.addEventListener('input', function(event) {
        const inputValue = event.target.value.trim();
        if (inputValue.length === 0) {
            suggestionElement.style.display = 'none';
            return;
        }

        fetch(`/api/v1/flights/suggest-city/${inputValue}/`)
            .then(response => response.json())
            .then(data => {
                suggestionElement.innerHTML = '';
                if (data.length > 0) {
                    suggestionElement.style.display = 'block';
                    data.forEach(suggestion => {
                        const option = document.createElement('option');
                        option.textContent = suggestion.name;
                        option.value = suggestion.name;
                        suggestionElement.appendChild(option);
                    });
                } else {
                    suggestionElement.style.display = 'none';
                }
            })
            .catch(error => console.error('Error fetching suggestions:', error));
    });

    suggestionElement.addEventListener('change', function(event) {
        inputElement.value = event.target.value;
        suggestionElement.style.display = 'none';
    });
}

const departureInput = document.getElementById('departure');
const departureSuggestions = document.getElementById('departure-suggestions');

handleInputSuggestions(departureInput, departureSuggestions);

const arrivalInput = document.getElementById('arrival');
const arrivalSuggestions = document.getElementById('arrival-suggestions');

handleInputSuggestions(arrivalInput, arrivalSuggestions);
