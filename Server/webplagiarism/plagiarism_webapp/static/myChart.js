function createChart(l1, l2, l3, v1, v2, v3) {

    // Definisco i dati da mostrare nel grafico
    var data = {
    labels: [l1, l2, l3],
    datasets: [
    {
    label: "Metrics",
    fillColor: "rgba(99,240,220,0.2)",
    strokeColor: "rgba(99,240,220,1)",
    data: [v1, v2, v3],
    }
    ]

    };

    // Ottengo il contesto 2D del Canvas in cui mostrare il grafico
    var ctx = document.getElementById("myBarChart").getContext("2d");

    // Crea il grafico e visualizza i dati
    var myBarChart = new Chart(ctx).Bar(data, {
      animation:false,
      scaleOverride:true,
      scaleSteps:10,
      scaleStartValue:0,
      scaleStepWidth:10,

    });  // opzioni per la scala custom
}