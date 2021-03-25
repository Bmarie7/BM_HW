// from data.js
var tableData = data;

// YOUR CODE HERE!
// Use D3 to select the table body
tbody = d3.select("tbody")

function display(data) {
    tbody.text("")
    data.forEach(function(sighting) {
        new_tr = tbody.append("tr")
        Object.entries(sighting).forEach(function([key, value]) {
            new_td = new_tr.append("td").text(value)
        })
    })
}

display(tableData)

var inputData = d3.select("#datetime")
var button = d3.select("filter-btn")

function searchButton() {
    d3.event.preventDefault();

    console.log(inputData.property("value"));

    var new_table = tableData.filter(sighting => sighting.datetime === inputData.property("value"))

    display(new_table);
}

inputData.on("change", searchButton)