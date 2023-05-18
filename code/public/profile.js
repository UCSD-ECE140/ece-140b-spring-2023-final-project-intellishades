document.addEventListener("DOMContentLoaded", init);


async function init() {
    // Obtain all existing sections from the slidespace
    fetch("/userinfo").then(response => {
        return response.json();
    }).then(json => {
        // Only get section information if the data is not null
        if(Object.keys(json).length > 0) {
            let userFirstName = document.querySelector(".user-first-name");
            let userLastName = document.querySelector(".user-last-name");
            let userEmail = document.querySelector(".user-email");
            let username = document.querySelector(".user-username");

            userFirstName.innerHTML = `First Name: ${json[0]}`;
            userLastName.innerHTML = `Last Name: ${json[1]}`;
            userEmail.innerHTML = `Email: ${json[2]}`;
            username.innerHTML = `Current Username: ${json[3]}`;

        }
    });
    populatePage();
}

// Assign functionality to HTML elements
function populatePage() {
    let updateInfoForm = document.querySelector(".update-user-form");
    if (updateInfoForm) {
        updateInfoForm.addEventListener('submit', (event) => {
            // Stop the default form behavior
            event.preventDefault();
            // Grab the needed form fields
            const action = "/updateuser";
            const method = "PUT";
            const data = Object.fromEntries(new FormData(updateInfoForm).entries());
            // Submit the PUT request
            server_request(action, data, method, (response) => {
                if (response.session_id != 0) {
                    location.replace('/login');
                }
                else {
                    alert("Modification failed! Please retry.");
                    updateInfoForm.reset();
                }
            });
        });
    }
    let deleteUserButton = document.querySelector(".delete-user");
    if (deleteUserButton) {
        deleteUserButton.addEventListener('click', (event) => {
            // Stop the default form behavior
            event.preventDefault();
            // Grab the needed form fields
            const action = "/deleteuser";
            const method = "DELETE";
            let data = {};
            // Submit the POST request
            server_request(action, data, method, (response) => {
                if (response.session_id != 0) {
                    location.replace('/');
                }
                else {
                    alert("Deletion failed! Please retry.");
                    updateInfoForm.reset();
                }
            });
        })
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