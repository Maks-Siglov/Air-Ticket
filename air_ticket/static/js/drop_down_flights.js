
document.addEventListener("DOMContentLoaded", function () {
    const dropdownButton = document.getElementById("orderStatusDropdownButton");
    const dropdownMenu = document.getElementById("orderStatusDropdownMenu");

    dropdownButton.addEventListener("click", function () {
        dropdownMenu.classList.toggle("show");
    });

    window.addEventListener("click", function (event) {
        if (!event.target.matches("#orderStatusDropdownButton") && !event.target.closest("#orderStatusDropdownMenu")) {
            dropdownMenu.classList.remove("show");
        }
    });
});