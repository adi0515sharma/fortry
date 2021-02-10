var hours = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23];
// For drawing the lines

var todaysData = [5, 6, 7, 8, 7, 6, 5, 6, 7, 9, 10, 9, 8, 7, 9, 10];
var yesterdaysData = [0, 1, 3, 4, 3, 2, 2, 2, 1, 3, 4];



var ctx = document.getElementById("myDashboardChart").getContext('2d');


var gradientFill = ctx.createLinearGradient(0, 0, 300, 0);
gradientFill.addColorStop(0, "rgba(51, 204, 255, 0.5)");
gradientFill.addColorStop(1, "rgba(255, 255, 255, 0.5)");

var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: hours,

        datasets: [

            {
                data: todaysData,
                label: "Today",
                // borderColor: "#3e95cd",
                borderColor: '#33ccff',
                lineTension: 0.1,
                backgroundColor: gradientFill
            },
            {
                data: yesterdaysData,
                label: "Yesterday",
                lineTension: 0.1,
                borderColor: "#a6a6a6",
                fill: false

            }
        ]
    },
    options: {
        legend: {
            align: 'center',
            // textDirection: 'rtl',
            position: 'bottom',
            labels: {
                boxWidth: 10
            }
        },
        scales: {
            xAxes: [{
                gridLines: {
                    color: "rgba(0, 0, 0, 0)",
                }
            }],
            yAxes: [{
                gridLines: {
                    color: "rgba(0, 0, 0, 0)",
                }
            }]
        }
    }
});


/* ---------------------------------- GRAPH END-----------------------------------------------------*/

