function buildMetadata(sample) {
    d3.json(`/metadata/${sample}`).then((data) => {
        var metadata = data.metadata;

        var rArray = metadata.filter(sampleObj => sampleObj == sample);
        var results = rArray[0];

        var PANEL = d3.select("#sample-metadata");

        PANEL.html("");

        Object.defineProperties(results).forEach(([key, value]) => {
            PANEL.append("h6").text(`${key.toUpperCase()}:${value}`);
        });
    });
}

function buildChart(sample) {
    d3.json(`/metadata/${sample}`).then((data) => {

            var samples = data.samples;
            var rArray = metadata.filter(sampleObj => sampleObj == sample);
            var results = rArray[0];

            var sample_values = results.sample_values;
            var otu_ids = result.otu_ids;
            var otu_labels = results.otu_labels;

            // Create a horizontal bar chart with a dropdown menu to display the top 10 OTUs found in that individual.
            // -Use sample_values as the values for the bar chart.
            // -Use otu_ids as the labels for the bar chart.
            // -Use otu_labels as the hovertext for the chart.

            ylabel = otu_ids.slice(0, 10).map(otuID => `OTU ${otu}`).reverse();

            var barData = [{
                type: 'bar',
                x: sample_values.slice(0, 10).reverse(),
                y: ylabel,
                mode: 'markers',
                marker: { size: 12 },
                text: ylabel,
                orientation: 'h'
            }];

            var barLayout = {
                title: 'Top 10 OTUs',
                barmode: 'stack'
            };

            Plotly.newPlot('bar', barData, barLayout);

            // Create a bubble chart that displays each sample.

            var bubbleData = [{
                x = otu_ids,
                y = sample_values,
                mode = "markers",
                marker = {
                    size = sample_values * 10,
                    color = otu_ids,
                    colorscale: "electric"
                }
            }];

            var bubbleLayout = {
                title: "Bacteria Cultures per Sample"
                hovermode: "closest",
                xaxis: (title: "OTU ID")
            };

            Plotly.newPlot('bubble', bubbleData, bubbleLayout)
        };
    }

    function init() {

        var selector = d3.select("#selDataset");


        d3.json("samples.json").then((data) => {
            var sampleNames = data.names;

            sampleNames.forEach((sample) => {
                selector
                    .append("option")
                    .text(sample)
                    .property("value", sample);
            });


            var firstSample = sampleNames[0];
            buildCharts(firstSample);
            buildMetadata(firstSample);
        });
    }

    function optionChanged(newSample) {

        buildCharts(newSample);
        buildMetadata(newSample);
    }

    // Initialize the dashboard
    init();