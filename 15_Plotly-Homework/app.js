function buildMetadata(sample) {

    var url = ("samples.json");
    // Use d3,json to get the metadata
    d3.json(url).then((data) => {

        let metadata = data.metadata;

        var sorting = metadata.filter(sampleObj => sampleObj.id == sample);
        var result = sorting[0];

        var sampleData = d3.select("#sample-metadata");

        // Use .html("") to clear exisiting data
        sampleData.html("");

        // Use Object.entries to add each key and value pair to sampleData
        Object.entries(result).forEach([key, value] => {
            sampleData.append("h6").text(`${key}:${value}`);
        });

    })
}

function buildCharts(sample) {
    d3.json(url).then((data) => {
        var x_value = result.otu_ids
        var y_value = result.otu_labels
        var marker_sz = result.sample_values
        var marker_c = otu_ids
        var textVal = otu_labels

        var samples = data.samples;
        var sorting = metadata.filter(sampleObj => sampleObj.id == sample);
        var result = sorting[0];

        // Build Bubble Chart
        var trace1 = {
            x: x_value,
            y: y_value,
            text: textVal,
            mode: 'markers',
            marker: {
                color: marker_c,
                colorscale: "Electric"
                size: marker_sz,
            }
        };

        var info = [trace1];

        var layout = {
            title: "Bacteria Cultures Per Sample",
        };
        Plotly.newPlot("bubble", info, layout);
    })
}

function init() {
    var selector = d3.select("#selDataset");

    d3.json(url).then((data) => {
        var nameSample = data.names;

        nameSample.forEach((sample) => {
            selector
                .append('option')
                .text(sample)
                .property('value', sample);
        });


        const firstSample = nameSample[0]
        buildCharts(firstSample)
        buildMetadata(firstSample)
    });
}

function optionChanged(newSample) {

    buildCharts(newSample);
    buildMetadata(newSample);
}

// Initialize the dashboard
init();