export function initUpdatingWidgetData() {
    updateWidgetConfig();
    updateWeatherWidget();
    updateSpotifyWidget();
    updateCalendarWidget();
    updateClockWidget();
    updateWebcamWidget();
    updateSystemWidget();
    updateGmailWidget();
}

// Widget Positions

async function updateWidgetConfig() {
    const socket = new WebSocket("ws://localhost:8000/ws/settings/widgets");

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);

        try {
            const { widgets: config } = data;

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
    };

    socket.onerror = (error) => {
        console.error("Widget Websocket Error: ", error)
    }
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
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/spotify");

    const spotifyDiv = document.getElementById('spotify');
    const titleEl = spotifyDiv?.querySelector('.title');
    const artistEl = spotifyDiv?.querySelector('.artist');
    const currentTimeEl = spotifyDiv?.querySelector('.current-time');
    const totalTimeEl = spotifyDiv?.querySelector('.total-time');
    const albumCoverEl = spotifyDiv?.querySelector('.album-cover');
    const nextArtistEl = spotifyDiv?.querySelector('.next-artist');
    const nextTitleEl = spotifyDiv?.querySelector('.next-title');

    const setFallbackValues = () => {
        if (titleEl) titleEl.textContent = "";
        if (artistEl) artistEl.textContent = "";
        if (currentTimeEl) currentTimeEl.textContent = "";
        if (totalTimeEl) totalTimeEl.textContent = "";
        if (albumCoverEl) albumCoverEl.textContent = "";
        if (nextArtistEl) nextArtistEl.textContent = "";
        if (nextTitleEl) nextTitleEl.textContent = "";
    };

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const {
                title = "",
                artist = "",
                current_time = "",
                total_time = "",
                album_cover = "",
                next_artist = "",
                next_title = ""
            } = data;

            if (!title || !artist || !current_time || !total_time || !album_cover || !next_artist || !next_title) {
                setFallbackValues();
                return;
            }

            if (spotifyDiv) {
                spotifyDiv.dataset.title = title;
                spotifyDiv.dataset.artist = artist;
                spotifyDiv.dataset.current_time = current_time;
                spotifyDiv.dataset.total_time = total_time;
                spotifyDiv.dataset.album_cover = album_cover;
                spotifyDiv.dataset.next_artist = next_artist;
                spotifyDiv.dataset.next_title = next_title;
            }

            if (titleEl) titleEl.textContent = title;
            if (artistEl) artistEl.textContent = artist;
            if (currentTimeEl) currentTimeEl.textContent = current_time;
            if (totalTimeEl) totalTimeEl.textContent = total_time;
            if (albumCoverEl) albumCoverEl.textContent = album_cover;
            if (nextArtistEl) nextArtistEl.textContent = next_artist;
            if (nextTitleEl) nextTitleEl.textContent = next_title;
        } catch (err) {
            console.error("Invalid data received:", err);
            setFallbackValues();
        }
    };

    socket.onerror = (error) => {
        console.error("Spotify WebSocket error:", error);
        setFallbackValues();
    };

    socket.onclose = () => {
        console.warn("Spotify WebSocket closed.");
        setFallbackValues();
    };
}

function updateCalendarWidget() {
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/calendar");

    const calendarDiv = document.getElementById('calendar');
    const dateEl = calendarDiv?.querySelector('.date');
    const firstDayEl = calendarDiv?.querySelector('.first-day');
    const eventTitlesEl = calendarDiv?.querySelector('.event-titles');

    const setFallbackValues = () => {
        if (dateEl) dateEl.textContent = "";
        if (firstDayEl) firstDayEl.textContent = "";
        if (eventTitlesEl) eventTitlesEl.textContent = "";
    };

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const {
                date = "",
                first_day = "",
                event_titles = "",
            } = data;

            if (!date || !first_day || !event_titles) {
                setFallbackValues();
                return;
            }

            if (calendarDiv) {
                calendarDiv.dataset.date = date;
                calendarDiv.dataset.first_day = first_day;
                calendarDiv.dataset.event_titles = event_titles;
            }

            if (dateEl) dateEl.textContent = date;
            if (firstDayEl) firstDayEl.textContent = first_day;
            if (eventTitlesEl) eventTitlesEl.textContent = event_titles;
        } catch (err) {
            console.error("Invalid data received:", err);
            setFallbackValues();
        }
    };

    socket.onerror = (error) => {
        console.error("Calendar WebSocket error:", error);
        setFallbackValues();
    };

    socket.onclose = () => {
        console.warn("Calendar WebSocket closed.");
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
        console.error("Clock WebSocket error:", error);
        setFallbackValues();
    };

    socket.onclose = () => {
        console.warn("Clock WebSocket closed.");
        setFallbackValues();
    };
}

function updateSystemWidget() {
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/system");

    const systemDiv = document.getElementById('system');
    const cpuEl = systemDiv?.querySelector('.cpu');
    const gpuEl = systemDiv?.querySelector('.gpu');
    const ramEl = systemDiv?.querySelector('.ram');
    const diskEl = systemDiv?.querySelector('.disk');

    const setFallbackValues = () => {
        if (cpuEl) cpuEl.textContent = "Location Not Found";
        if (gpuEl) gpuEl.textContent = "_";
        if (ramEl) ramEl.textContent = "_";
        if (diskEl) diskEl.textContent = "Description Not Found";
    };

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const {
                cpu_usage = "",
                gpu_usage = "",
                ram_usage = "",
                disk_usage = ""
            } = data;

            if (!cpu_usage || !gpu_usage || !ram_usage || !disk_usage) {
                setFallbackValues();
                return;
            }

            if (systemDiv) {
                systemDiv.dataset.cpu_usage = cpu_usage;
                systemDiv.dataset.gpu_usage = gpu_usage;
                systemDiv.dataset.ram_usage = ram_usage;
                systemDiv.dataset.disk_usage = disk_usage;
            }

            if (cpuEl) cpuEl.textContent = cpu_usage;
            if (gpuEl) gpuEl.textContent = gpu_usage;
            if (ramEl) ramEl.textContent = ram_usage;
            if (diskEl) diskEl.textContent = disk_usage;
        } catch (err) {
            console.error("Invalid data received:", err);
            setFallbackValues();
        }
    };

    socket.onerror = (error) => {
        console.error("System WebSocket error:", error);
        setFallbackValues();
    };

    socket.onclose = () => {
        console.warn("System WebSocket closed.");
        setFallbackValues();
    };
}

function updateGmailWidget() {
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/gmail");

    const gmailDiv = document.getElementById('gmail');
    const sendersEl = gmailDiv?.querySelector('.senders');
    const headersEl = gmailDiv?.querySelector('.headers');
    const profileEl = gmailDiv?.querySelector('.profile');

    const setFallbackValues = () => {
        if (sendersEl) sendersEl.textContent = "No Unread Emails!";
        if (headersEl) headersEl.textContent = "Good Job :)";
        if (profileEl) profileEl.textContent = "";
    };

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const {
                headers = "",
                senders = "",
                profile = ""
            } = data;

            if (!headers || !senders || !profile) {
                setFallbackValues();
                return;
            }

            if (gmailDiv) {
                gmailDiv.dataset.headers = headers;
                gmailDiv.dataset.senders = senders;
                gmailDiv.dataset.profile = profile;
            }

            if (sendersEl) sendersEl.textContent = senders;
            if (headersEl) headersEl.textContent = headers;
            if (profileEl) profileEl.textContent = profile;
        } catch (err) {
            console.error("Invalid data received:", err);
            setFallbackValues();
        }
    };

    socket.onerror = (error) => {
        console.error("Gmail WebSocket error:", error);
        setFallbackValues();
    };

    socket.onclose = () => {
        console.warn("Gmail WebSocket closed.");
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