document.addEventListener("DOMContentLoaded", init);
// Define table data
var tableData = [
    ['', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'],
    ['12:00-1:00 AM', '', '', '', '', '', '', ''],
    ['1:00-2:00 AM', '', '', '', '', '', '', ''],
    ['2:00-3:00 AM', '', '', '', '', '', '', ''],
    ['3:00-4:00 AM', '', '', '', '', '', '', ''],
    ['4:00-5:00 AM', '', '', '', '', '', '', ''],
    ['5:00-6:00 AM', '', '', '', '', '', '', ''],
    ['6:00-7:00 AM', '', '', '', '', '', '', ''],
    ['7:00-8:00 AM', '', '', '', '', '', '', ''],
    ['8:00-9:00 AM', '', '', '', '', '', '', ''],
    ['9:00-10:00 AM', '', '', '', '', '', '', ''],
    ['10:00-11:00 AM', '', '', '', '', '', '', ''],
    ['11:00-12:00 AM', '', '', '', '', '', '', ''],
    ['12:00-1:00 PM', '', '', '', '', '', '', ''],
    ['1:00-2:00 PM', '', '', '', '', '', '', ''],
    ['2:00-3:00 PM', '', '', '', '', '', '', ''],
    ['3:00-4:00 PM', '', '', '', '', '', '', ''],
    ['4:00-5:00 PM', '', '', '', '', '', '', ''],
    ['5:00-6:00 PM', '', '', '', '', '', '', ''],
    ['6:00-7:00 PM', '', '', '', '', '', '', ''],
    ['7:00-8:00 PM', '', '', '', '', '', '', ''],
    ['8:00-9:00 PM', '', '', '', '', '', '', ''],
    ['9:00-10:00 PM', '', '', '', '', '', '', ''],
    ['10:00-11:00 PM', '', '', '', '', '', '', ''],
    ['11:00-12:00 PM', '', '', '', '', '', '', '']
];

var currentCellStatus = [];
for (let i = 0; i < 24; i++) {
    currentCellStatus[i] = [];
    for (let j = 0; j < 7; j++) {
        currentCellStatus[i][j] = 0; // Set schedule to black on default
    }
}
var allCellElements = [];
for (let i = 0; i < 24; i++) {
    allCellElements[i] = [];
    for (let j = 0; j < 7; j++) {
        allCellElements[i][j] = 0; // Initialize the array of elements with placeholders
    }
}
var BlueisClicked = false;
var BlackisClicked = false;
var dimisClicked = false;
var buttonColor;

function init() { //only for things that are slow 
    // Button to choose window mode
    const blueButton = document.getElementById("blueButton");
    const dimButton = document.getElementById("dimButton");
    const blackButton = document.getElementById("blackButton");
    const confirmButton = document.getElementById("confirmButton");

    var BlueOriginalColor = blueButton.style.backgroundColor;
    var BlackOriginalColor = blackButton.style.backgroundColor;
    var dimOriginalColor = dimButton.style.backgroundColor;
    

    blackButton.addEventListener("click", function () {
        if (BlackisClicked) {
            blackButton.style.backgroundColor = BlackOriginalColor;
            blackButton.style.color = "#2C3531";
            BlackisClicked = false;
        } else {
            blackButton.style.backgroundColor = "#2C3531";
            blackButton.style.color = "white";
            BlackisClicked = true;
            buttonColor = "black"
        }
        blueButton.style.backgroundColor = BlueOriginalColor;
        BlueisClicked = false;

        dimButton.style.backgroundColor = dimOriginalColor;
        dimisClicked = false;
    });

    blueButton.addEventListener("click", function () {
        if (BlueisClicked) {
            blueButton.style.backgroundColor = BlueOriginalColor;
            BlueisClicked = false;
        } else {
            blueButton.style.backgroundColor = "#D1E8E2";
            BlueisClicked = true;
            buttonColor = "blue"
        }
        blackButton.style.backgroundColor = BlackOriginalColor;
        blackButton.style.color = "#2C3531";
        BlackisClicked = false;

        dimButton.style.backgroundColor = dimOriginalColor;
        dimisClicked = false;
    });

    dimButton.addEventListener("click", function () {
        if (dimisClicked) {
            dimButton.style.backgroundColor = dimOriginalColor;
            dimisClicked = false;
        } else {
            dimButton.style.backgroundColor = "#D9B08C";
            dimisClicked = true;
            buttonColor = "dim"
        }
        blackButton.style.backgroundColor = BlackOriginalColor;
        blackButton.style.color = "#2C3531";
        BlackisClicked = false;

        blueButton.style.backgroundColor = BlueOriginalColor;
        BlueisClicked = false;
    });

    // Get the table div element
    var tableDiv = document.getElementById("schedulingTable");

    // Create a table element and add it to the table div
    var table = document.createElement("table");
    tableDiv.appendChild(table);

    // Create table rows and cells and add them to the table
    for (let i = 0; i < tableData.length; i++) {
        var row = document.createElement("tr");
        for (let j = 0; j < tableData[i].length; j++) {
            var cell = document.createElement("td");
            cell.innerText = tableData[i][j];
            if (i > 0 && j > 0) {
                // Save the reference to the cell element
                allCellElements[i - 1][j - 1] = cell;
                // Add event listener to cell
                var isMouseDown = false;
                cell.addEventListener("mousedown", function () {
                    isMouseDown = true;
                    //this.classList.add(buttonColor);
                    cell_status_update(i, j);
                });
                cell.addEventListener("mouseover", function () {
                    if (isMouseDown) {
                        //this.classList.add(buttonColor);
                        cell_status_update(i, j);
                    }
                });
                cell.addEventListener("mouseup", function () {
                    isMouseDown = false;
                    cell_status_update(i, j);
                });

                // Make it OFF on default
                cell.classList.add("black");

            }
            row.appendChild(cell);
        }
        table.appendChild(row);
        //console.log("JS current cells:", currentCellStatus);
    }

    confirmButton.addEventListener("click", function () {
        // send current schedule to mysql and pi
        sendScheduleToDevice()
    });

        // call get route that fetchs previously saved data 
    //setTimeout(function () {
        fetch("/schedule_data_website", {
            credentials: 'same-origin', // 'include', default: 'omit'
            method: 'GET',
            body: null,
            headers: new Headers({
                "Content-Type": "application/json",
                "Accept": "application/json, text-plain, */*",
                "X-Requested-With": "XMLHttpRequest"
            })
        })
            .then((response) => response.json())
            .then((data) => {
                //console.log("schedule data after get route:" , data);
                currentCellStatus = data["schedule"];
                updateAllCells(BlueOriginalColor, BlackOriginalColor, dimOriginalColor);
                // console.log("cell status after get route", currentCellStatus);
            })
            .catch((error) => {
                console.error(error);
            });
    //}, 5000);
}

// Update all the cells after the new schedule is retrieved from the device
function updateAllCells() {
    for (let i = 0; i < tableData.length - 1; i++) {
        for (let j = 0; j < tableData[i].length - 1; j++) {
            if (currentCellStatus[i][j] == 0) {
                allCellElements[i][j].classList.add("black");
                allCellElements[i][j].classList.remove("blue");
                allCellElements[i][j].classList.remove("dim");
            } else if (currentCellStatus[i][j] == 2) {
                allCellElements[i][j].classList.remove("black");
                allCellElements[i][j].classList.add("blue");
                allCellElements[i][j].classList.remove("dim");
            } else if (currentCellStatus[i][j] == 1) {
                allCellElements[i][j].classList.remove("black");
                allCellElements[i][j].classList.remove("blue");
                allCellElements[i][j].classList.add("dim");
            }
        }
    }
}

function cell_status_update(i, j) {
    const hour = i - 1;
    const day = j - 1;
    if (BlackisClicked) { // If the user selected black to adjust
        currentCellStatus[hour][day] = 0;
        allCellElements[hour][day].classList.add("black");
        allCellElements[hour][day].classList.remove("blue");
        allCellElements[hour][day].classList.remove("dim");
        console.log("black clicked:", currentCellStatus);
    } else if (BlueisClicked) { // If the user selected transparent to adjust
        console.log("current status hour day:", hour, day);
        currentCellStatus[hour][day] = 2;
        allCellElements[hour][day].classList.add("blue");
        allCellElements[hour][day].classList.remove("black");
        allCellElements[hour][day].classList.remove("dim");
        console.log("transparent clicked:", currentCellStatus);
    } else if (dimisClicked) { // If the user selected dim to adjust
        currentCellStatus[hour][day] = 1;
        allCellElements[hour][day].classList.remove("black");
        allCellElements[hour][day].classList.remove("blue");
        allCellElements[hour][day].classList.add("dim");
        console.log("dim clicked:", currentCellStatus);
    }
}


function sendScheduleToDevice() {
    console.log("current cell status", currentCellStatus);
    currentCell_dict = {"device_id": 99, // Placeholder Device ID
                        "user_id": 000, //Placeholder User ID
                        "schedule": currentCellStatus}
    server_request("/update_schedule", currentCell_dict, 'POST');
}

// Define the 'request' function to handle interactions with the server
function server_request(url, data = {}, verb, callback) {
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
        .then(function (response) {
            if (callback)
                callback(response);
        })
        .catch(error => console.error('Error:', error));
}