// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyCIuQ9cSsOyBdxzRsFUUG1cxEEwAVMQ3Uw",
    authDomain: "datameasuringdb.firebaseapp.com",
    databaseURL: "https://datameasuringdb-default-rtdb.firebaseio.com",
    projectId: "datameasuringdb",
    storageBucket: "datameasuringdb.appspot.com",
    messagingSenderId: "554867866432",
    appId: "1:554867866432:web:6a56c089f49aecd53ed8a5",
    measurementId: "G-SZJQ83WFP1"
};
// Initialize Firebase
firebase.initializeApp(firebaseConfig);

// Reference to the sensor_data node
const database = firebase.database();
const sensorDataRef = database.ref('sensor_data');

// Get buttons and display area
const startButton = document.getElementById('startButton');
const stopButton = document.getElementById('stopButton');

// Variables to hold the Firebase listener reference
let dataListener = null;

// Create the charts for each sensor data type
const temperatureChart = new Chart(document.getElementById('temperatureChart').getContext('2d'), createChartConfig('Temperature', 'rgb(255, 99, 132)'));
const humidityChart = new Chart(document.getElementById('humidityChart').getContext('2d'), createChartConfig('Humidity', 'rgb(54, 162, 235)'));
const lightIntensityChart = new Chart(document.getElementById('lightIntensityChart').getContext('2d'), createChartConfig('Light Intensity', 'rgb(255, 206, 86)'));
const heightChart = new Chart(document.getElementById('heightChart').getContext('2d'), createChartConfig('Height', 'rgb(75, 192, 192)'));

// Function to create chart configuration
function createChartConfig(label, color) {
    return {
        type: 'line',
        data: {
            labels: [],  // X-axis labels (timestamps)
            datasets: [{
                label: label,
                borderColor: color,
                data: [],  // Sensor values
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                x: {
                    type: 'time',  // Use time scale for the X-axis
                    time: {
                        unit: 'minute',  // Adjust this to your needs
                        tooltipFormat: 'MMM d, yyyy, h:mm:ss a',  // Tooltip format
                        displayFormats: {
                            second: 'h:mm:ss a',
                            minute: 'h:mm a',
                            hour: 'MMM d, h a',
                            day: 'MMM d'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Time'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Value'
                    }
                }
            }
        }
    };
}

// Function to start fetching data
function startFetching() {
    // Attach a listener to fetch data
    dataListener = sensorDataRef.on('child_added', (snapshot) => {
        const data = snapshot.val();
        addDataToCharts(data);
    });

    // Disable Start button and enable Stop button
    startButton.disabled = true;
    stopButton.disabled = false;
}

// Function to stop fetching data
function stopFetching() {
    // Remove the Firebase listener
    sensorDataRef.off('child_added', dataListener);

    // Disable Stop button and enable Start button
    startButton.disabled = false;
    stopButton.disabled = true;
}

// Function to add data to all charts
function addDataToCharts(data) {
    // Convert timestamp to Date object
    const timestamp = new Date(data.timestamp * 1000);

    // Add new data points to each chart
    temperatureChart.data.labels.push(timestamp);
    temperatureChart.data.datasets[0].data.push(data.temperature);

    humidityChart.data.labels.push(timestamp);
    humidityChart.data.datasets[0].data.push(data.humidity);

    lightIntensityChart.data.labels.push(timestamp);
    lightIntensityChart.data.datasets[0].data.push(data.lightIntensity);

    heightChart.data.labels.push(timestamp);
    heightChart.data.datasets[0].data.push(data.height);

    // Update all charts with the new data
    temperatureChart.update();
    humidityChart.update();
    lightIntensityChart.update();
    heightChart.update();
}

// Add event listeners to the buttons
startButton.addEventListener('click', startFetching);
stopButton.addEventListener('click', stopFetching);
