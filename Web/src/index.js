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
        xValues.push(measurements[i][3]);
        y_temp_Values.push(measurements[i][1]);
        y_hum_Values.push(measurements[i][2]);
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
        table.innerHTML += "<tr><th>Id</th><th>Sonde</th><th>Latitude</th><th>Longitude</th></tr>"

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

        console.log(api);
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


async function getChartValuesBySensor() {

    const sensors = await getSensorsResponse();
    console.log(sensors);
    data = []
    for (let i = 0; i < sensors.length; i++) {
        sensor_id = sensors[i][0]
        console.log(sensor_id);
//        const measures = await getMeasuresResponseBySensor(sensor_id);
//        console.log(measures);
        data.push({
        'sensor':sensors[i][0],
//        'sensor': getMeasuresResponseBySensor(sensor_id),
        })
    }
    console.log(data);


//    const measurements = await getMeasuresResponseBySensor();
//    const xValues = [];
//    const y_temp_Values = [];
//    const y_hum_Values = [];
//
//
//    for (let i = 0; i < measurements.length; i++) {
//        xValues.push(measurements[i][3]);
//        y_temp_Values.push(measurements[i][1]);
//        y_hum_Values.push(measurements[i][2]);
//    }

}
getChartValues();
getSensorTableValues();
getChartValuesBySensor();