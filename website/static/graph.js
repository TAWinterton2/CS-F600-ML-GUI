// Import values from the html that called the script
var graph = document.getElementById("graph");
var chartName = graph.getAttribute("name");
var pyData = JSON.parse(graph.getAttribute("data"));
var ctx = document.getElementById(chartName).getContext('2d');
var columns = JSON.parse(graph.getAttribute("columns"))

// Create new chart utilizing DataFrame values
new Chart(ctx, {
    type: "scatter",
    data: {
        datasets: [{
            pointRadius: 4,
            pointBackgroundColor: "rgb(0,0,255)",
            backgroundColor: "rgb(0,0,255)",
            data: pyData,
            label: chartName,
        }
    ]},
    options: {
        scales: {
            x: {
                title: {
                    display: true,
                    text: columns[0],
                }
            },
            y: {
                title: {
                    display: true,
                    text: columns[1],
                }
            }
        }
    }
});