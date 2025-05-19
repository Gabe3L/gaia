export function initUpdatingWidgetData() {
    updateWidgetConfig();
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