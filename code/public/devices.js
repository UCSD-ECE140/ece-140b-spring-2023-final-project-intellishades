document.addEventListener("DOMContentLoaded", init);

async function init() {
    /*
    await fetch("/protected").then(response => {
        return response.json();
    }).then(json => {
        // Only get section information if the data is not null
        if(json["message"] == 'Access granted') {
            // The user is logged in. Need to verify their identity
            // TODO: Check if the device is linked under this user
        }
    });*/
    let manageDeviceButton = document.querySelector(".manage-device-button");
    let device_id = 0; // Placeholder for test device
    manageDeviceButton.addEventListener('click', manageTestDevice(device_id));
}

function manageTestDevice(device_id) {
    console.log("Now managing device");
    fetch(`/manage_device/${device_id}`);
}