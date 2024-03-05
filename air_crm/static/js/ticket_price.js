document.addEventListener("DOMContentLoaded", function () {
    function updatePriceForForm(form) {
        const priceInput = form.querySelector('#id_price');
        const seatTypeRadios = form.querySelectorAll('input[name="seat_type"]');
        const lunchCheckbox = form.querySelector('#lunchOption');
        const luggageCheckbox = form.querySelector('#luggageOption');

        function updatePrice() {
            let price = 0;

            seatTypeRadios.forEach(radio => {
                if (radio.checked) {
                    if (radio.value === 'Economy') price += 120;
                    else if (radio.value === 'Business') price += 250;
                    else if (radio.value === 'First Class') price += 450;
                }
            });

            if (lunchCheckbox.checked) price += 10;
            if (luggageCheckbox.checked) price += 30;

            priceInput.value = price;
        }

        seatTypeRadios.forEach(radio => {
            radio.addEventListener('change', updatePrice);
        });
        lunchCheckbox.addEventListener('change', updatePrice);
        luggageCheckbox.addEventListener('change', updatePrice);

        updatePrice();
    }

    document.querySelectorAll('#ticketForm').forEach(form => {
        updatePriceForForm(form);
    });
});