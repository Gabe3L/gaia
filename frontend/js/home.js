const threadStates = {
    camera: false,
    speech_to_text: false,
    text_to_speech: false,
    performing_actions: false,
};

function toggleThread(name) {
    if (!(name in threadStates)) {
        updateStatus(`Unknown thread: ${name}`);
        return;
    }

    const isRunning = threadStates[name];
    const endpoint = isRunning ? `/stop-thread/${name}` : `/start-thread/${name}`;

    fetch(endpoint, { method: 'POST' })
        .then(response => {
            if (!response.ok) throw new Error(`Server returned ${response.status}`);
            return response.json();
        })
        .then(data => {
            threadStates[name] = !isRunning;
            const action = isRunning ? "Stopped" : "Started";
            updateStatus(`${action} ${formatThreadName(name)} thread.`);
        })
        .catch(err => {
            updateStatus(`Error toggling ${formatThreadName(name)}: ${err.message}`);
        });
}

function formatThreadName(name) {
    return name
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

function updateStatus(msg) {
    const statusDiv = document.getElementById('statusMessages');
    const newEntry = document.createElement('p');
    newEntry.textContent = msg;
    statusDiv.appendChild(newEntry);
    statusDiv.scrollTop = statusDiv.scrollHeight;
}

function updateGAIAResponse(text) {
    const responseBox = document.getElementById('gaiaResponse');
    responseBox.innerHTML = `<p>${text}</p>`;
}

const webcam = document.getElementById('webcam');
navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(stream => { webcam.srcObject = stream; })
    .catch(err => {
        updateStatus(`Webcam error: ${err.message}`);
    });
