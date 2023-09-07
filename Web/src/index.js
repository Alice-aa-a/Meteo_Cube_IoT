async function getMeasuresResponse() {
    try {
        const response = await fetch('http://127.0.0.1:5000/get_all_measures');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const measurements = await response.json();
        return measurements;
        }
        catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }

async function getChartValues() {
    const measurements = await getMeasuresResponse();
    const xValues = [];
    const y_temp_Values = [];
    const y_hum_Values = [];

    for (let i = 0; i < measurements.length; i++) {
        date = new Date(measurements[i]['date'])
        date = new Date(date.getTime()+date.getTimezoneOffset()*60*1000);
        var options = { year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric',
        };
        date = date.toLocaleDateString('fr-FR', options);
        xValues.push(date);
        y_temp_Values.push(measurements[i]['temperature']);
        y_hum_Values.push(measurements[i]['humidity']);
    }

    new Chart("myChart", {
      type: "line",
      data: {
        labels: xValues,
        datasets: [{
          label: 'Température',
          fill: false,
          lineTension: 0,
          backgroundColor: "rgba(249, 61, 61, 0.8)",
          borderColor: "rgba(249, 61, 61, 0.8)",
          data: y_temp_Values
        },
        {
          label: 'Humidité',
          fill: false,
          lineTension: 0,
          backgroundColor: "rgba(61, 206, 249, 0.8)",
          borderColor: "rgba(61, 206, 249, 0.8)",
          data: y_hum_Values
        }]
      },
      options: {
        legend: {
            display: true,
         },
        scales: {
          yAxes: [{ticks: {min: -10, max:100}}],
        }
      }
    });
    }


async function getSensorsResponse() {
    try {
        const response = await fetch('http://127.0.0.1:5000/get_all_sensors');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const sensors = await response.json();
        return sensors;
        }
        catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }

async function getSensorTableValues() {

    const sensors = await getSensorsResponse();

    var table = document.getElementById("sensor_table");
        table.innerHTML += "<tr><th>Id</th><th>Sonde</th><th>Latitude (°)</th><th>Longitude (°)</th></tr>"

    for (let i = 0; i < sensors.length; i++) {
        table.innerHTML += '<tr><td>' +
        sensors[i][0].toString() + '</td><td>'+
        sensors[i][1].toString() + '</td><td>'+
        sensors[i][2].toString() + '</td><td>'+
        sensors[i][3].toString() + '</td></tr>'
    }
}

async function getMeasuresResponseBySensor(sensor_id) {
    try {
        api = "http://127.0.0.1:5000/get_sensor_measure/%s" % (sensor_id)

        const response = await fetch(api);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const measurements = await response.json();
        return measurements;
        }
        catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }

async function getMeasureTableValues() {

    const measures = await getMeasuresResponse();

    var table = document.getElementById("measures_table");
        table.innerHTML += "<tr><th>Id</th><th>Température (°C)</th><th>Humidité (%)</th><th>Date</th><th>ID Sonde</th></tr>"
    for (let i = 0; i < measures.length; i++) {

        date = new Date(measures[i]['date'])
        date = new Date(date.getTime()+date.getTimezoneOffset()*60*1000);
        var options = { year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric',
        };
        date = date.toLocaleDateString('fr-FR', options);
        temp_value = measures[i]['temperature']
        str = '<td>'
        if (temp_value > 19) {
            str = "<td class='text-bg-danger'>"
        }
        if (temp_value < 5) {
            str = "<td class='text-bg-primary'>"
        }
        table.innerHTML += '<tr><td>' +
        measures[i]['id'].toString() + '</td>'+ str +
        measures[i]['temperature'].toString() + '</td><td>'+
        measures[i]['humidity'].toString() + '</td><td>'+
        date.toString() + '</td><td>'+
        measures[i]['sensor_id'].toString() + '</td></tr>'
    }
}

getChartValues();
getSensorTableValues();
getMeasureTableValues();