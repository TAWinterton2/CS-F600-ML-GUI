// Import values from the html that called the script
var graph = document.getElementById("pred_graph");
var chartName = graph.getAttribute("name");
var pyData = JSON.parse(graph.getAttribute("data"));
var columns = JSON.parse(graph.getAttribute("columns"))
var ctx = document.getElementById(chartName).getContext('2d');
var pred = JSON.parse(graph.getAttribute("pred"));

// Create new chart utilizing DataFrame values
new Chart(ctx, {
    type: "scatter",
    data: 
    {
        datasets: [
        {
            type: "scatter",
            pointRadius: 4,
            pointBackgroundColor: "rgb(0,0,255)",
            backgroundColor: "rgb(0,0,255)",
            data: pyData,
            label: "Actual Y Values"
        },
        {
            type: "line",
            data: pred,
            backgroundColor: "rgb(255, 0, 0)",
            borderColor: "rgb(255, 0, 0)",
            xScale: 'x2',
            showLine: true,
            pointRadius: 0,
            fill: false,
            label: "Predicted Y Values"
        }
    ]
    },
    options: 
    {
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