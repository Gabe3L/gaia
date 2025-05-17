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

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const {
                location = "No Location",
                temperature = "",
                precipitation = "",
                description = ""
            } = data;

            if (!location || !temperature || !precipitation || !description) {
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
        }
    };

    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
    };

    socket.onclose = () => {
        console.warn("Weather WebSocket closed.");
    };
}

function updateSpotifyWidget() {
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/spotify");

    const spotifyDiv = document.getElementById('spotify');
    const titleEl = spotifyDiv?.querySelector('.title');
    const artistEl = spotifyDiv?.querySelector('.artist');
    const currentTimeEl = spotifyDiv?.querySelector('.current-time');
    const totalTimeEl = spotifyDiv?.querySelector('.total-time');
    const albumNameEl = spotifyDiv?.querySelector('.album-name');
    const albumCoverEl = spotifyDiv?.querySelector('.album-cover');
    const nextArtistEl = spotifyDiv?.querySelector('.next-artist');
    const nextTitleEl = spotifyDiv?.querySelector('.next-title');

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const {
                title = "No Playback",
                current_time = "0:00",
                total_time = "0:00",
                next_artist = "No Artist",
                next_title = "Queue Empty",
                album_name = "Unknown Album",
                artist = "Unknown Artist",
                album_cover = null
            } = data;

            if (!title || !current_time || !total_time || !next_artist || !next_title || !artist || !album_name || !album_cover) {
                return;
            }

            if (spotifyDiv) {
                spotifyDiv.dataset.title = title;
                spotifyDiv.dataset.current_time = current_time;
                spotifyDiv.dataset.total_time = total_time;
                spotifyDiv.dataset.next_artist = next_artist;
                spotifyDiv.dataset.next_title = next_title;
                spotifyDiv.dataset.artist = artist;
                spotifyDiv.dataset.album_name = album_name;
                spotifyDiv.dataset.album_cover = album_cover;
            }

            if (titleEl) titleEl.textContent = title;
            if (artistEl) artistEl.textContent = artist;
            if (currentTimeEl) currentTimeEl.textContent = current_time;
            if (totalTimeEl) totalTimeEl.textContent = total_time;
            if (nextArtistEl) nextArtistEl.textContent = next_artist;
            if (nextTitleEl) nextTitleEl.textContent = next_title;
            if (albumNameEl) albumNameEl.textContent = next_artist;
            if (albumCoverEl) albumCoverEl.src = album_cover;

            const fillEl = spotifyDiv?.querySelector('.playback-fill');
            if (fillEl && current_time && total_time) {
                const timeToSeconds = (timeStr) => {
                    const [mins, secs] = timeStr.split(':').map(Number);
                    return (mins * 60) + secs;
                };

                const currentSeconds = timeToSeconds(current_time);
                const totalSeconds = timeToSeconds(total_time);

                const percent = Math.min((currentSeconds / totalSeconds) * 100, 100);
                fillEl.style.width = `${percent}%`;
            }
        } catch (err) {
            console.error("Invalid data received:", err);
        }
    };

    socket.onerror = (error) => {
        console.error("Spotify WebSocket error:", error);
    };

    socket.onclose = () => {
        console.warn("Spotify WebSocket closed.");
    };
}

function updateCalendarWidget() {
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/calendar");

    const calendarDiv = document.getElementById('calendar');
    const dateEl = calendarDiv?.querySelector('.date');
    const firstDayEl = calendarDiv?.querySelector('.first-day');
    const eventTitlesEl = calendarDiv?.querySelector('.event-titles');

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const {
                date = "",
                first_day = "",
                event_titles = "",
            } = data;

            if (!date || !first_day || !event_titles) {
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
        }
    };

    socket.onerror = (error) => {
        console.error("Calendar WebSocket error:", error);
    };

    socket.onclose = () => {
        console.warn("Calendar WebSocket closed.");
    };
}

function updateClockWidget() {
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/clock");

    const clockDiv = document.getElementById('clock');
    const timeEl = clockDiv?.querySelector('.time');
    const dateEl = clockDiv?.querySelector('.date');

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const {
                time = "00:00",
                date = "Date Unknown"
            } = data;

            if (!time || !date) {
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
        }
    };

    socket.onerror = (error) => {
        console.error("Clock WebSocket error:", error);
    };

    socket.onclose = () => {
        console.warn("Clock WebSocket closed.");
    };
}

function updateSystemWidget() {
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/system");

    const systemDiv = document.getElementById('system');
    const cpuEl = systemDiv?.querySelector('.cpu');
    const gpuEl = systemDiv?.querySelector('.gpu');
    const ramEl = systemDiv?.querySelector('.ram');
    const diskEl = systemDiv?.querySelector('.disk');

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
        }
    };

    socket.onerror = (error) => {
        console.error("System WebSocket error:", error);
    };

    socket.onclose = () => {
        console.warn("System WebSocket closed.");
    };
}

function updateGmailWidget() {
    const socket = new WebSocket("ws://127.0.0.1:8000/ws/gmail");

    const gmailDiv = document.getElementById('gmail');
    const sendersEl = gmailDiv?.querySelector('.senders');
    const headersEl = gmailDiv?.querySelector('.headers');
    const profileEl = gmailDiv?.querySelector('.profile');

    socket.onmessage = (event) => {
        try {
            const data = JSON.parse(event.data);
            const {
                headers = "No Unread Emails!",
                senders = "Good Job :)",
                profile = ""
            } = data;

            if (!headers || !senders || !profile) {
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
        }
    };

    socket.onerror = (error) => {
        console.error("Gmail WebSocket error:", error);
    };

    socket.onclose = () => {
        console.warn("Gmail WebSocket closed.");
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