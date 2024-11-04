// login.js

document.getElementById('loginForm').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the form from submitting normally

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const data = {
        username: username,
        password: password
    };

    fetch('http://127.0.0.1:8000/coach_nutr/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);
        // Handle successful login here (e.g., redirect to a different page)
        window.location = 'http://127.0.0.1:8000/coach_nutr/dashboard/';
    })
    .catch((error) => {
        console.error('Error:', error);
        // Show an error message to the user
    });
});
