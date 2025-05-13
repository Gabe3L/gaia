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

export function initUpdatingWidgetData() {
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/weather");

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        const { location, temperature, precipitation, description } = data;

        const weatherDiv = document.getElementById('weather');
        if (!weatherDiv) return;

        weatherDiv.style.setProperty('--location', `"${location}"`);
        weatherDiv.style.setProperty('--temperature', `"${temperature} °C"`);
        weatherDiv.style.setProperty('--precipitation', `"${precipitation} %"`);
        weatherDiv.style.setProperty('--description', `"${description}"`);
    };

    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
    };

    socket.onclose = () => {
        console.warn("Weather WebSocket closed.");
    };

    const webcamDiv = document.getElementById('webcam');
    if (!webcamDiv) return;
    navigator.mediaDevices.getUserMedia({ video: true, audio: false })
        .then(stream => { webcamDiv.srcObject = stream; })
        .catch(err => {
            console.error(`Webcam error: ${err.message}`);
        });
}