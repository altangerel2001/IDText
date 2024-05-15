// Project 2: myapp/static/myapp/main.js
function uploadImage() {
    const imageInput = document.getElementById('imageInput');
    const file = imageInput.files[0];

    if (file) {
        const reader = new FileReader();
        reader.onloadend = function() {
            const base64Image = reader.result.split(',')[1];

            fetch('/process_image/', {
                method: 'POST',
                body: JSON.stringify({ image: base64Image }),
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                } else {
                    document.getElementById('extractedText').innerText = data.extracted_text;
                    document.getElementById('surname').innerText = data.surname;
                    document.getElementById('givenName').innerText = data.given_name;
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        };
        reader.readAsDataURL(file);
    } else {
        alert('Please select an image file.');
    }
}

// Function to get CSRF token from cookies
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
