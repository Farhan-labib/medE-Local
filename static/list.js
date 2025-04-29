function AddToList(user, p_id) {
    const morningCheckbox = document.querySelector('input[name="MorningD"]');
    const dayCheckbox = document.querySelector('input[name="DayD"]');
    const nightCheckbox = document.querySelector('input[name="NightD"]');
    const numDays = parseInt(document.getElementById('DayNumSpan').value) || 0;
    
    const isMorningChecked = morningCheckbox.checked;
    const isDayChecked = dayCheckbox.checked;
    const isNightChecked = nightCheckbox.checked;
    
    const intakes = [];
    if (isMorningChecked) intakes.push("Morning");
    if (isDayChecked) intakes.push("Day");
    if (isNightChecked) intakes.push("Night");
    
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    
    const data = {
        user: user,
        p_id: p_id,
        intakes: intakes,
        numDays: numDays
    };
    
    fetch('/save_med_list/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        /* Handle response */
    })
    .catch(error => {
        /* Handle errors */
    });
}

document.querySelectorAll('input[type="checkbox"], input[type="text"]').forEach((input) => {
    input.addEventListener('change', () => {
       updateDataAndSendRequest(input.closest('tr'));
    });
});

document.querySelectorAll('.day-decrease-btn').forEach((button) => {
    button.addEventListener('click', () => {
        let row = button.closest('tr');
        let numInput = row.querySelector('.num');
        let currentValue = parseInt(numInput.value);
        if (currentValue > 1) {
            numInput.value = currentValue - 1;
            updateDataAndSendRequest(row);
        }
    });
});

document.querySelectorAll('.day-increase-btn').forEach((button) => {
    button.addEventListener('click', () => {
        let row = button.closest('tr');
        let numInput = row.querySelector('.num');
        let currentValue = parseInt(numInput.value);
        numInput.value = currentValue + 1;
        updateDataAndSendRequest(row);
    });
});

function updateDataAndSendRequest(row) {
    let updatedData = gatherUpdatedDataFromTable(row);
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
     
    fetch('/save_med_list/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(updatedData)
    })
    .then(response => response.json())
    .then(data => {
        /* Handle response */
    })
    .catch(error => {
        /* Handle errors */
    });
}

function gatherUpdatedDataFromTable(row) {
    let medicineId = row.dataset.productName;
        
    let morningCheckbox = row.querySelector('input[name="MorningD"]');
    let dayCheckbox = row.querySelector('input[name="DayD"]');
    let nightCheckbox = row.querySelector('input[name="NightD"]');
    let dayNumInput = row.querySelector('.num');
    
    let intakes = [];
    if (morningCheckbox.checked) {
        intakes.push('Morning');
    }
    if (dayCheckbox.checked) {
        intakes.push('Day');
    }
    if (nightCheckbox.checked) {
        intakes.push('Night');
    }
    
    let numDays = parseInt(dayNumInput.value);
    
    let updatedData = {
        user: getUserPhoneNumber(),
        p_id: medicineId,
        intakes: intakes,
        numDays: numDays
    };
    
    return updatedData;
}

document.querySelectorAll('.remove-button').forEach(button => {
    button.addEventListener('click', function() {
        const productId = this.getAttribute('data-product-id');
        handleRemoveProduct(productId);
    });
});

function handleRemoveProduct(productId) {
    fetch(`/remove_productList/${productId}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(),
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const rowToRemove = document.querySelector(`tr[data-product-name="${productId}"]`);
            if (rowToRemove) {
                rowToRemove.remove();
            }
        }
    })
    .catch(error => {
        /* Handle errors */
    });
}

function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}

function getUserPhoneNumber() {
    return userPhoneNumber;
}