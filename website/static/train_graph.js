// Import values from the html that called the script
var graph = document.getElementById("train_graph");
var chartName = graph.getAttribute("name");
var pyData = JSON.parse(graph.getAttribute("data"));
var ctx = document.getElementById(chartName).getContext('2d');

// Create new chart utilizing DataFrame values
new Chart(ctx, {
    type: "scatter",
    data: 
    {
        datasets: [
            {
            pointRadius: 4,
            pointBackgroundColor: "rgb(0,255,0)",
            backgroundColor: "rgb(0,255,0)",
            data: pyData,
            label: chartName
        }
    ]
    },
    options: 
    {
        legend: 
        {
            display: true,
        },
        scales: 
        {
            x: 
            {
                beginAtZero: true
            }
        }
    }
});