import * as widgets from '/static/js/widgets.js';

const threadStates = {
    camera: false,
    speech_to_text: false,
    text_to_speech: false,
    performing_actions: false,
};

function toggleThread(name) {
    if (!(name in threadStates)) {
        console.error(`Unknown thread: ${name}`);
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
            console.info(`${action} ${formatThreadName(name)} thread.`);
        })
        .catch(err => {
            console.error(`Error toggling ${formatThreadName(name)}: ${err.message}`);
        });
}

function formatThreadName(name) {
    return name
        .split('_')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

document.addEventListener('DOMContentLoaded', function () {
    console.log("DOM is fully loaded");

    widgets.initUpdatingWidgetData();
}); 