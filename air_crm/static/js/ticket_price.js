const priceInput = document.getElementById('id_price');
const seatTypeRadios = document.querySelectorAll('input[name="seat_type"]');
const lunchCheckbox = document.getElementById('lunchOption');
const luggageCheckbox = document.getElementById('luggageOption');

    function updatePrice() {
        let price = 0; // Base price

        // Seat type price adjustments
        seatTypeRadios.forEach(radio => {
            if (radio.checked) {
                if (radio.value === 'economy') price += 120;
                else if (radio.value === 'business') price += 250;
                else if (radio.value === 'first_class') price += 450;
            }
        });

        // Additional options price adjustments
        if (lunchCheckbox.checked) price += 10;
        if (luggageCheckbox.checked) price += 30;

        priceInput.value = price ;
    }

    // Update price when selections change
    seatTypeRadios.forEach(radio => {
        radio.addEventListener('change', updatePrice);
    });
    lunchCheckbox.addEventListener('change', updatePrice);
    luggageCheckbox.addEventListener('change', updatePrice);

    updatePrice();