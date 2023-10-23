function AddToList(user, p_id) {
    const morningCheckbox = document.querySelector('input[name="MorningD"]');
    const dayCheckbox = document.querySelector('input[name="DayD"]');
    const nightCheckbox = document.querySelector('input[name="NightD"]');
    const numDays = parseInt(document.getElementById('Daynum').innerText) || 0;

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


document.querySelectorAll('input[type="checkbox"], input[type="text"]').forEach((input) => {
    input.addEventListener('change', () => {
        // Get the updated data from the table
        let updatedData = gatherUpdatedDataFromTable(input.closest('tr'));
        console.log(updatedData);
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
    });
});

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








// function fetchSavedList() {
//     console.log("Its Loaded");

//     // Get the user phone number with the '+' sign and encode it
//     const userPhoneNumber = encodeURIComponent(getUserPhoneNumber());
//     // Inside your JavaScript code where you want to fetch the saved data
//     fetch(`/get_saved_data/?user=${userPhoneNumber}`)
//     .then(response => response.json())
//     .then(data => {
//         // Handle the fetched data here
//         console.log(data);
//         // Populate your table or perform other operations with the data
//     })
//     .catch(error => {
//         // Handle errors if the request fails
//         console.error('Error:', error);
//     });
// }



// Function to get the user's phone number from wherever it's stored
function getUserPhoneNumber() {
    return userPhoneNumber;
}



// // Function to populate the table with the retrieved data
// function populateTable(data) {
//     const tbody = document.getElementById('medListBody');

//     // Clear existing table rows
//     tbody.innerHTML = '';

//     // Iterate through the data and create table rows
//     data.forEach(item => {
//         const tr = document.createElement('tr');
//         const tdProductName = document.createElement('td');
//         tdProductName.textContent = item.productName; // Replace 'productName' with the key where product name is stored in your data
//         const tdTimes = document.createElement('td');
//         // Create checkboxes based on item.times (assuming it's an array of times)
//         item.times.forEach(time => {
//             const checkbox = document.createElement('input');
//             checkbox.type = 'checkbox';
//             checkbox.checked = true; // You can set the checked status based on your data
//             const label = document.createElement('label');
//             label.textContent = time;
//             tdTimes.appendChild(checkbox);
//             tdTimes.appendChild(label);
//         });
//         const tdDays = document.createElement('td');
//         tdDays.textContent = item.days; // Replace 'days' with the key where number of days is stored in your data

//         // Append table cells to the row
//         tr.appendChild(tdProductName);
//         tr.appendChild(tdTimes);
//         tr.appendChild(tdDays);

//         // Append the row to the table body
//         tbody.appendChild(tr);
//     });
// }

// Call fetchSavedData() when your page is ready to load the saved data into the table
// document.addEventListener('DOMContentLoaded', function () {
//     fetchSavedList();
// });


