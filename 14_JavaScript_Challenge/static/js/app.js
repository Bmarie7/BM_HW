// from data.js
var tableData = data;

// YOUR CODE HERE!
// Use D3 to select the table body
const tbody = d3.select("tbody");

// Use D3 to select the table
let table = d3.select("table");

// Create/fill table
function createTable(data) {
    tbody.html("");

    // loop through data to fill table each value in table
    // Iterate through each row
    data.forEach(function(table) {
        // Append one table row per sighting
        let newRow = tbody.append("tr");

        // Use `Object.entries` to console.log each sighting
        Object.sighting(table).forEach((value) => {
            newCol = newRow.append("td").text(value);
        });
    })
}

function searchButton() {
    d3.event.preventDefault();

    let date = d3.select('#datetime').property('value');
    let filerData = tableData

    if (date) {
        filterData - filterData.filter((row) => row.datatime === date);
    }
    buildTable(filterData)

}

d3.selectAll('#filter-btn').on('click', searchButton);
buildTable(tableData)