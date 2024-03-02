function handleUpload() {
    const fileInput = document.getElementById("file-upload");
    const selectedDays = getSelectedDays();

    const formData = new FormData();
    formData.append("prescription_image", fileInput.files[0]);

    // Append the "selected_days" data to the formData object
    for (const day of selectedDays) {
        formData.append("selected_days", day);
    }

    // Get the CSRF token from a cookie (you may need to adjust the cookie name)
    const csrfToken = getCookie("csrftoken");

    $.ajax({
        type: "POST",
        url: '/upload_prescription/', // Update this with your URL
        data: formData,
        processData: false,
        contentType: false,
        headers: {
            "X-CSRFToken": csrfToken // Set the CSRF token as a request header
        },
        success: function(response) {
            window.location.href = '/prescription_confirm/';
        },
        error: function(error) {
            // Handle any errors
        }
    });
}


// Function to get the CSRF token from a cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getSelectedDays() {
    const checkboxes = document.querySelectorAll(".days input[type=checkbox]");
    const selectedDays = [];

    checkboxes.forEach(checkbox => {
        if (checkbox.checked) {
            selectedDays.push(checkbox.value);
        }
    });

    return selectedDays;
}

