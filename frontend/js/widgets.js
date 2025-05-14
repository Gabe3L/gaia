export async function applyWidgetConfig() {
    try {
        const response = await fetch('/static/config/widgets.json');
        const { widgets: config } = await response.json();

        for (const [id, data] of Object.entries(config)) {
            const el = document.getElementById(id);
            if (!el) continue;

            if (!data.visible) {
                el.style.display = 'none';
                continue;
            }

            el.style.display = '';

            const { gridWidth, gridHeight, xLocation, yLocation } = data;

            if (
                gridWidth != null &&
                gridHeight != null &&
                xLocation != null &&
                yLocation != null
            ) {
                el.style.gridColumnStart = xLocation + 1;
                el.style.gridColumnEnd = `span ${gridWidth}`;
                el.style.gridRowStart = yLocation + 1;
                el.style.gridRowEnd = `span ${gridHeight}`;
            } else {
                el.style.gridColumn = '';
                el.style.gridRow = '';
            }
        }
    } catch (error) {
        console.error('Failed to apply widget configuration:', error);
    }
}

export function initUpdatingWidgetData() {
    updateWeatherWidget();
    updateWebcamWidget();
}

// Custom Widgets

function updateWeatherWidget() {
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/weather");

    const weatherDiv = document.getElementById('weather');
    const locationEl = weatherDiv?.querySelector('.location');
    const temperatureEl = weatherDiv?.querySelector('.temperature');
    const precipitationEl = weatherDiv?.querySelector('.precipitation');
    const descriptionEl = weatherDiv?.querySelector('.description');

    const setFallbackValues = () => {
        if (locationEl) locationEl.textContent = "Location Not Found";
        if (temperatureEl) temperatureEl.textContent = "_";
        if (precipitationEl) precipitationEl.textContent = "_";
        if (descriptionEl) descriptionEl.textContent = "Description Not Found";
    };

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const {
                location = "",
                temperature = "",
                precipitation = "",
                description = ""
            } = data;

            if (!location || !temperature || !precipitation || !description) {
                setFallbackValues();
                return;
            }

            if (weatherDiv) {
                weatherDiv.dataset.location = location;
                weatherDiv.dataset.temperature = temperature;
                weatherDiv.dataset.precipitation = precipitation;
                weatherDiv.dataset.description = description;
            }

            if (locationEl) locationEl.textContent = location;
            if (temperatureEl) temperatureEl.textContent = `${temperature} °C`;
            if (precipitationEl) precipitationEl.textContent = `${precipitation} %`;
            if (descriptionEl) descriptionEl.textContent = description;
        } catch (err) {
            console.error("Invalid data received:", err);
            setFallbackValues();
        }
    };

    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
        setFallbackValues();
    };

    socket.onclose = () => {
        console.warn("Weather WebSocket closed.");
        setFallbackValues();
    };
}

function updateWebcamWidget() {
    const webcamDiv = document.getElementById('webcam');
    if (!webcamDiv) return;
    navigator.mediaDevices.getUserMedia({ video: true, audio: false })
        .then(stream => { webcamDiv.srcObject = stream; })
        .catch(err => {
            console.error(`Webcam error: ${err.message}`);
        });
}