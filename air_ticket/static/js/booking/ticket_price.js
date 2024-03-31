document.addEventListener("DOMContentLoaded", function () {
    function updatePriceForForm(form) {
        const priceInput = form.querySelector('#id_price');
        const lunchCheckbox = form.querySelector('#lunchOption');
        const luggageCheckbox = form.querySelector('#luggageOption');

        function updatePrice() {
            let price = 0;

            if (lunchCheckbox.checked) price += 10;
            if (luggageCheckbox.checked) price += 30;

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