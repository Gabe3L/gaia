export async function applyWidgetConfig() {
    try {
        const response = await fetch('/static/config/widgets.json');
        const config = await response.json();
        const widgets = document.querySelectorAll('.widgets .widget');

        config.widgets.forEach((widgetData, index) => {
            const el = widgets[index];
            if (!el) return;

            const { gridWidth, gridHeight } = widgetData;
            const { id } = widgetData;

            el.id = `${id}`;
            el.classList.add(`w-${gridWidth}`, `h-${gridHeight}`);
        });
    } catch (error) {
        console.error('Failed to apply widget configuration:', error);
    }
}

export function updateWidgetData() {
    const weatherDiv = document.getElementById('weather');
    if (!weatherDiv) return;

    fetch('http://127.0.0.1:8000/weather', {
        method: 'GET'
    })
        .then(response => {
            if (!response.ok) throw new Error('Network response error');
            return response.json();
        })
        .then(data => {
            const { location, temperature, precipitation, description } = data;

            weatherDiv.style.setProperty('--location', `"${location}"`);
            weatherDiv.style.setProperty('--temperature', `"${temperature} °C"`);
            weatherDiv.style.setProperty('--precipitation', `"${precipitation} %"`);
            weatherDiv.style.setProperty('--description', `"${description} °C"`);
        })
        .catch(error => {
            console.error('Error fetching weather data:', error);
        });

    const webcamDiv = document.getElementById('webcam');
    if (!webcamDiv) return;
    navigator.mediaDevices.getUserMedia({ video: true, audio: false })
        .then(stream => { webcamDiv.srcObject = stream; })
        .catch(err => {
            console.error(`Webcam error: ${err.message}`);
        });
}