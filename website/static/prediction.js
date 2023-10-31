// Import values from the html that called the script
var graph = document.getElementById("pred_graph");
var chartName = graph.getAttribute("name");
var pyData = JSON.parse(graph.getAttribute("data"));
var ctx = document.getElementById(chartName).getContext('2d');
var pred = JSON.parse(graph.getAttribute("pred"));

console.log(chartName);
console.log(pyData);
console.log(pred);
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
            data: pyData,
        },
        {
            type: "line",
            data: pred,
            backgroundColor: "rgb(255, 0, 0)",
            borderColor: "rgb(255, 0, 0)",
            xScale: 'x2',
            showLine: true,
            pointRadius: 1,
        }
    ]
    },
    options: 
    {
        legend: 
        {
            display: false
        },
        scales: 
        {
            x: 
            {
                beginAtZero: true,
                ticks: {
                    stepSize: 1,
                }
            },
            x2: {
                position: 'bottom',
                type: 'category'
            }
        }
    }
});