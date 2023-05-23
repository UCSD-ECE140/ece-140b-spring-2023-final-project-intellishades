document.addEventListener("DOMContentLoaded", init);

// Define table data as global
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
// Globals to let cellFunctionality() know which value to update for that cell
var transparentButtonClicked = false;
var blackButtonClicked = false;
var dimButtonClicked = false;
var currentCellStatus = [];

function init () { //only for things that are slow 
    // Button to choose window mode
    const transparentButton = document.getElementById("blueButton");
    const dimButton = document.getElementById("dimButton");
    const blackButton = document.getElementById("blackButton");
    //var buttonColor;
    //var BlueOriginalColor = transparentButton.style.backgroundColor;
    //var BlackOriginalColor = blackButton.style.backgroundColor;
    //var DimOriginalColor = dimButton.style.backgroundColor;

    blackButton.addEventListener("click", function () {
        if (blackButtonClicked) {
            //blackButton.style.backgroundColor = BlackOriginalColor;
            //blackButton.style.color = "#2C3531";
            blackButtonClicked = false;
            transparentButtonClicked = false;
            dimButtonClicked = false;
        } else {
            //blackButton.style.backgroundColor = "#2C3531";
            //blackButton.style.color = "white";
            //buttonColor = "black"
            blackButtonClicked = true;
            transparentButtonClicked = false;
            dimButtonClicked = false;
        }
    });

    transparentButton.addEventListener("click", function () {
        if (transparentButtonClicked) {
            //transparentButton.style.backgroundColor = BlueOriginalColor;
            blackButtonClicked = false;
            transparentButtonClicked = false;
            dimButtonClicked = false;
        } else {
            //transparentButton.style.backgroundColor = "#D1E8E2";
            //buttonColor = "blue"
            blackButtonClicked = false;
            transparentButtonClicked = true;
            dimButtonClicked = false;
        }
    });

    dimButton.addEventListener("click", function () {
        if (dimButtonClicked) {
            blackButtonClicked = false;
            transparentButtonClicked = false;
            dimButtonClicked = false;
        } else {
            blackButtonClicked = false;
            transparentButtonClicked = false;
            dimButtonClicked = true;
        }
    });

    populateTable();
    
}

// Populate the table elements
function populateTable() {
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
                });
                cell.addEventListener("mouseover", function () {
                    if (isMouseDown) {
                        this.classList.toggle(buttonColor);
                    }
                });
                cell.addEventListener("mouseup", function () {
                    isMouseDown = false;
                    cellFunctionality(i - 1, j - 1); // Add functionality to the cell
                });
            }
            row.appendChild(cell);
        }
        table.appendChild(row);
    }
}

/**
 * This functionality updates the cell's status on the global variable 
 * @param int hour, the hour to modify by clicking the cell
 * @param int day, the day to modify by clicking the cell
 */
function cellFunctionality(hour, day) {
    // Do not modify cell data if no state is selected by the user
    if (blackButtonClicked) { // If the user selected black to adjust
        currentCellStatus[hour][day] = 0;
    } else if (transparentButtonClicked) { // If the user selected transparent to adjust
        currentCellStatus[hour][day] = 2;
    } else if (dimButtonClicked) { // If the user selected dim to adjust
        currentCellStatus[hour][day] = 1;
    }
}