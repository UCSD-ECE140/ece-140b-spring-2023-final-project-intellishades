document.addEventListener("DOMContentLoaded", function () { //only for things that are slow 
    // Button to choose window mode
    const blueButton = document.getElementById("blueButton");
    const dimButton = document.getElementById("dimButton");
    const blackButton = document.getElementById("blackButton");
    var buttonColor;

    var BlueOriginalColor = blueButton.style.backgroundColor;
    var BlueisClicked = false;
    var BlackOriginalColor = blackButton.style.backgroundColor;
    var BlackisClicked = false;
    var dimOriginalColor = dimButton.style.backgroundColor;
    var dimisClicked = false;

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
    });


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

    // Get the table div element
    var tableDiv = document.getElementById("myTable");

    // Create a table element and add it to the table div
    var table = document.createElement("table");
    tableDiv.appendChild(table);

    // Create table rows and cells and add them to the table
    for (var i = 0; i < tableData.length; i++) {
        var row = document.createElement("tr");
        for (var j = 0; j < tableData[i].length; j++) {
            var cell = document.createElement("td");
            cell.innerText = tableData[i][j];
            if (i > 0 && j > 0) {
                // Add event listener to cell
                var isMouseDown = false;
                cell.addEventListener("mousedown", function () {
                    isMouseDown = true;
                    this.classList.toggle(buttonColor);
                    cell_status_update(i, j);
                });
                cell.addEventListener("mouseover", function () {
                    if (isMouseDown) {
                        this.classList.toggle(buttonColor);
                    }
                    cell_status_update(i, j);
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
    }

    function cell_status_update(i, j) {
        let hour = i - 1;
        let day = j - 1;
        if (blackButtonClicked) { // If the user selected black to adjust
            currentCellStatus[hour][day] = 0;
            this.classList.add("black");
            this.classList.remove("blue");
            this.classList.remove("dim");
        } else if (transparentButtonClicked) { // If the user selected transparent to adjust
            currentCellStatus[hour][day] = 2;
            this.classList.add("blue");
            this.classList.remove("black");
            this.classList.remove("dim");
        } else if (dimButtonClicked) { // If the user selected dim to adjust
            currentCellStatus[hour][day] = 1;
            this.classList.remove("black");
            this.classList.remove("blue");
            this.classList.add("dim");
        }
    }

    function sendScheduleToDevice() {
        let dataToSend = {
            'device_id': 999,
            'user_id': 000,
            'schedule': currentCellStatus
        };
        server_request("/update_schedule", dataToSend, 'POST');
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
});