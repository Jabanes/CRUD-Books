
const SERVER = "http://127.0.0.1:5000"
axios.get(SERVER).then(res=> console.log(res.data))

document.addEventListener("DOMContentLoaded", function () {
    const dropdowns = document.querySelectorAll(".dropdown > a");

    dropdowns.forEach(dropdown => {
        dropdown.addEventListener("click", function () {
            const menu = this.nextElementSibling;

            // Toggle the dropdown
            if (menu.style.display === "block") {
                menu.style.display = "none"; // Hide it if it's already open
            } else {
                // Hide all dropdowns
                document.querySelectorAll(".dropdown-menu").forEach(otherMenu => {
                    otherMenu.style.display = "none";
                });

                // Show the current menu
                menu.style.display = "block";
            }
        });
    });
});
