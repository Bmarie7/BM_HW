function buildMetadata(sample) {
    // use d3 to slect panel with ID
    d3.json(`/metadata/${sample}`).then((data) => {
        var metadata = data.metadata;

        var PANEL = d3.select("#sample-metadata");

        //clear any existing data
        PANEL.html("");

        Object.entries(data).forEach(([key, value]) => {
            PANEL.append("h6").text(`${key}:${value}`);
            console.log(key, value);
        });
    });
}

function buildChart(sample) {
    d3.json(`/samples/${sample}`).then((data) => {

            var sample_values = data.sample_values;
            var otu_ids = data.otu_ids;
            var otu_labels = data.otu_labels;
            console.log(otu_ids, otu_labels, sample_values);

            // Create a bubble chart that displays each sample.

            var bubbleData = [{
                x = otu_ids,
                y = sample_values,
                mode = "markers",
                marker = {
                    size = sample_values * 10,
                    color = otu_ids,
                    colorscale: "Electric"
                }
            }];

            var bubbleLayout = {
                title: "Bacteria Cultures per Sample",
                margin: { t: 0 },
                hovermode: "closest",
                xaxis: { title: "OTU ID" }
            };

            Plotly.newPlot('bubble', bubbleData, bubbleLayout);

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
        };
    }

    function init() {

        var selector = d3.select("#selDataset");

        d3.json("/names").then((sampleNames) => {
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