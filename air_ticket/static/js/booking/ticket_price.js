document.addEventListener("DOMContentLoaded", function () {
    function updatePriceForForm(form) {
        const priceInput = form.querySelector('#id_price');
        const lunchCheckbox = form.querySelector('#lunchOption');
        const luggageCheckbox = form.querySelector('#luggageOption');

        function updatePrice() {
            let price = flightPrice;

            if (lunchCheckbox.checked) price += lunchPrice;
            if (luggageCheckbox.checked) price += luggagePrice;

            priceInput.value = price;
        }

        lunchCheckbox.addEventListener('change', updatePrice);
        luggageCheckbox.addEventListener('change', updatePrice);

        updatePrice();
    }

    document.querySelectorAll('#ticketForm').forEach(form => {
        updatePriceForForm(form);
    });
});
