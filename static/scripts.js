// Wait for DOM to load
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");
    const loadingSpinner = document.createElement("div");

    // Add loading spinner
    loadingSpinner.id = "loading-spinner";
    loadingSpinner.style.display = "none";
    loadingSpinner.innerHTML = `
        <div class="spinner"></div>
        <p>Fetching data, please wait...</p>
    `;
    document.body.appendChild(loadingSpinner);

    // Form submission handler
    form.addEventListener("submit", (e) => {
        const ticker = document.querySelector("#ticker").value.trim();
        const startDate = document.querySelector("#start_date").value;
        const endDate = document.querySelector("#end_date").value;

        if (!ticker || !startDate || !endDate) {
            alert("Please fill in all fields!");
            e.preventDefault();
        } else {
            // Show spinner
            loadingSpinner.style.display = "block";
        }
    });
});
