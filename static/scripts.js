// Form validation
document.addEventListener('DOMContentLoaded', function () {
    const form = document.querySelector('form');
    form.addEventListener('submit', function (e) {
        const ticker = document.getElementById('ticker').value.trim();
        const startDate = document.getElementById('start_date').value;
        const endDate = document.getElementById('end_date').value;

        if (!ticker || !startDate || !endDate) {
            alert('Please fill out all fields.');
            e.preventDefault();
        }
    });
});