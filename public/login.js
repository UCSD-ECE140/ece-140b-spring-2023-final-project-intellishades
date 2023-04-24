document.addEventListener("DOMContentLoaded", init);


function init() {
    let login_form = document.getElementById("login-user-form");
    if (login_form) { // in case we are not on the login page
        login_form.addEventListener('submit', (event) => {
            // Stop the default form behavior
            event.preventDefault();
            // Grab the needed form fields
            const action = "/login";
            const method = "POST";
            const data = Object.fromEntries(new FormData(login_form).entries());
            // Submit the POST request
            server_request(action, data, method, (response) => {
                if (response.session_id != 0) {
                    location.replace('/dashboard');
                }
                else {
                    alert("Authentication failed! Please retry.");
                    login_form.reset();
                }
            });
        });
    }
}

// Define the 'request' function to handle interactions with the server
function server_request(url, data={}, verb, callback) {
    return fetch(url, {
                credentials: 'same-origin',
                method: verb,
                body: JSON.stringify(data),
                headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest'
                }
                })
                .then(response => response.json())
                .then(function(response) {
                if(callback)
                    callback(response);
                })
                .catch(error => console.error('Error:', error));
}