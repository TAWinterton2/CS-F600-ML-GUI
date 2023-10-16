// Import values from the html that called the script
var graph = document.getElementById("graph");
var chartName = graph.getAttribute("name");
var pyData = JSON.parse(graph.getAttribute("data"));
var ctx = document.getElementById(chartName).getContext('2d');

// Create new chart utilizing DataFrame values
new Chart(ctx, {
type: "scatter",
data: {
    datasets: [{
    pointRadius: 4,
    pointBackgroundColor: "rgb(0,0,255)",
    data: Object.values(pyData),
    labels: Object.keys(pyData)
    }]
},
options: {
    legend: {display: false},
    scales: {
        x: {
            beginAtZero: true
        }
    }
  }
});