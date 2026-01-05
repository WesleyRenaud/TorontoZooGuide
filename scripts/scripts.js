// Get elements
const mapPreset = document.getElementById('mapPreset');
const mapDateInput = document.getElementById('mapDate');

// Initialize Flatpickr on the input
const fp = flatpickr(mapDateInput, {
    defaultDate: new Date(),   // defaults to today
    dateFormat: "Y-m-d",       // matches YYYY-MM-DD
    allowInput: true,
    wrap: false,
    clickOpens: true,
    minDate: "today",          // optional: prevent past dates
    onChange: function(selectedDates, dateStr) {
        // Update map when a new date is picked
        updateMap(mapPreset.value, dateStr);
    }
});

// Show/hide date picker depending on dropdown selection
mapPreset.addEventListener('change', () => {
    if (mapPreset.value === 'today') {
        mapDateInput.style.display = 'inline-block';
    } else {
        mapDateInput.style.display = 'none';
    }
    updateMap(mapPreset.value, mapDateInput.value);
});

// Initialize visibility on page load
mapPreset.dispatchEvent(new Event('change'));
