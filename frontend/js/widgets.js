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
    updateSpotifyWidget();
    updateCalendarWidget();
    updateClockWidget();
    updateWebcamWidget();
    updateSystemWidget();
    updateGmailWidget();
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

function updateSpotifyWidget() {
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

function updateCalendarWidget() {
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

function updateClockWidget() {
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/clock");

    const clockDiv = document.getElementById('clock');
    const timeEl = clockDiv?.querySelector('.time');
    const dateEl = clockDiv?.querySelector('.date');

    const setFallbackValues = () => {
        if (timeEl) timeEl.textContent = "00:00";
        if (dateEl) dateEl.textContent = "Date Unknown";
    };

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const {
                time = "",
                date = ""
            } = data;

            if (!time || !date) {
                setFallbackValues();
                return;
            }

            if (clockDiv) {
                clockDiv.dataset.time = time;
                clockDiv.dataset.date = date;
            }

            if (timeEl) timeEl.textContent = time;
            if (dateEl) dateEl.textContent = date;
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
        console.warn("Clock WebSocket closed.");
        setFallbackValues();
    };
}

function updateSystemWidget() {
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/system");

    const weatherDiv = document.getElementById('system');
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

function updateGmailWidget() {
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/gmail");

    const weatherDiv = document.getElementById('weather');
    const sendersEl = weatherDiv?.querySelector('.senders');
    const headersEl = weatherDiv?.querySelector('.headers');

    const setFallbackValues = () => {
        if (sendersEl) sendersEl.textContent = "No Unread Emails!";
        if (headersEl) headersEl.textContent = "Good Job :)";
    };

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const {
                headers = "",
                senders = ""
            } = data;

            if (!headers || !senders) {
                setFallbackValues();
                return;
            }

            if (weatherDiv) {
                weatherDiv.dataset.headers = headers;
                weatherDiv.dataset.senders = senders;
            }

            if (sendersEl) sendersEl.textContent = senders;
            if (headersEl) headersEl.textContent = headers;
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