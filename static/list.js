function AddToList(user, p_id) {
    const morningCheckbox = document.querySelector('input[name="MorningD"]');
    const dayCheckbox = document.querySelector('input[name="DayD"]');
    const nightCheckbox = document.querySelector('input[name="NightD"]');
    const numDays = parseInt(document.getElementById('DayNumSpan').value) || 0;


    // Check if the checkboxes are checked or not
    const isMorningChecked = morningCheckbox.checked;
    const isDayChecked = dayCheckbox.checked;
    const isNightChecked = nightCheckbox.checked;

    const intakes = [];
    if (isMorningChecked) intakes.push("Morning");
    if (isDayChecked) intakes.push("Day");
    if (isNightChecked) intakes.push("Night");

    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

    // console.log('Intakes:', intakes);
    // console.log('NumDays:', numDays);
    // Prepare the data to be sent in the POST request
    const data = {
        user: user,
        p_id: p_id,
        intakes: intakes,
        numDays: numDays
    };
    // console.log("Data:", data)

    // Make a POST request to your server with CSRF token included
    fetch('/save_med_list/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken, // Include CSRF token for CSRF protection
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the server if needed
        console.log(data);
    })
    .catch(error => {
        // Handle errors if the request fails
        console.error('Error:', error);
    });
}



// Event listener for input fields and checkboxes
document.querySelectorAll('input[type="checkbox"], input[type="text"]').forEach((input) => {
    input.addEventListener('change', () => {
       updateDataAndSendRequest(input.closest('tr'));
    });
});

// Event listener for day-decrease-btn buttons
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

// Event listener for day-increase-btn buttons
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

    // Get the updated data from the specific row
    let updatedData = gatherUpdatedDataFromTable(row);
    // console.log(updatedData);
    const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
     
    fetch('/save_med_list/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken, // Include CSRF token for CSRF protection
        },
        body: JSON.stringify(updatedData)
    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the server if needed
        console.log(data);
    })
    .catch(error => {
        // Handle errors if the request fails
        console.error('Error:', error);
    });
}



function gatherUpdatedDataFromTable(row) {
    let medicineId = row.dataset.productName;
        
    // Extract checkbox states and input value from the row
    let morningCheckbox = row.querySelector('input[name="MorningD"]');
    let dayCheckbox = row.querySelector('input[name="DayD"]');
    let nightCheckbox = row.querySelector('input[name="NightD"]');
    let dayNumInput = row.querySelector('.num');

    // Prepare the data object for the current row
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

    // Add the current row's data to the updatedData array
    let updatedData = {
        user: getUserPhoneNumber(), // Replace with the actual user phone number
        p_id: medicineId,
        intakes: intakes,
        numDays: numDays
    };

    // console.log(updatedData);
    return updatedData;
}


document.querySelectorAll('.remove-button').forEach(button => {
    button.addEventListener('click', function() {
        const productId = this.getAttribute('data-product-id');
        // Call a function to handle the removal logic, passing the productId
        handleRemoveProduct(productId);
    });
});



function handleRemoveProduct(productId) {
    // Make a DELETE request to the backend API to remove the product
    // console.log("Removing Product ID: ",productId)
    fetch(`/remove_productList/${productId}/`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken(), // Include CSRF token for CSRF protection
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Successfully removed the product, update the DOM to remove the corresponding table row
            const rowToRemove = document.querySelector(`tr[data-product-name="${productId}"]`);
            if (rowToRemove) {
                rowToRemove.remove();
            }
            // console.log('Product removed successfully:', productId);
        } else {
            console.error('Failed to remove product:', data.error);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Function to get the CSRF token from the meta tag
function getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
}








// Function to get the user's phone number from wherever it's stored
function getUserPhoneNumber() {

    return userPhoneNumber;
};




