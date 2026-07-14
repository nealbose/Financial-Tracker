// Set today's date as default in date input
const dateInput = document.getElementById('date');
if (dateInput) {
    const today = new Date().toISOString().split('T')[0];
    dateInput.value = today;
}

// Set current month as default in month input
const monthInput = document.getElementById('month');
if (monthInput) {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    monthInput.value = `${year}-${month}`;
}

// Format currency inputs
const currencyInputs = document.querySelectorAll('input[type="number"]');
currencyInputs.forEach(input => {
    input.addEventListener('blur', function() {
        if (this.value) {
            this.value = parseFloat(this.value).toFixed(2);
        }
    });
});
