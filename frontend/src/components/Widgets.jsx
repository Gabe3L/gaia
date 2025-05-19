import { useState, useEffect } from "react";

import WeatherWidget from "./widgets/WeatherWidget";
import SpotifyWidget from "./widgets/SpotifyWidget";
import CalendarWidget from "./widgets/CalendarWidget";
import ClockWidget from "./widgets/ClockWidget";
import SystemWidget from "./widgets/SystemWidget";
import GmailWidget from "./widgets/GmailWidget";
import WebcamWidget from "./widgets/WebcamWidget";

export default function Widgets() {
  const [widgetConfig, setWidgetConfig] = useState({});

  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8000/ws/settings/widgets");
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.widgets) {
        setWidgetConfig(data.widgets);
      }
    };
    socket.onerror = (error) => {
      console.error("Widget Websocket Error: ", error);
    };

    return () => socket.close();
  }, []);

  const getStyle = (id) => {
    const config = widgetConfig[id];
    if (!config || !config.visible) return { display: "none" };

    const { gridWidth, gridHeight, xLocation, yLocation } = config;
    return {
      display: "",
      gridColumnStart: xLocation + 1,
      gridColumnEnd: `span ${gridWidth}`,
      gridRowStart: yLocation + 1,
      gridRowEnd: `span ${gridHeight}`,
    };
  };

  return (
    <div className="widgets">
      <div className="widgets" style={{ display: "grid" }}>
        <div id="weatherWidget" style={getStyle("weatherWidget")}>
          <WeatherWidget />
        </div>
      </div>
      <div className="widgets" style={{ display: "grid" }}>
        <div id="weatherWidget" style={getStyle("weatherWidget")}>
          <SpotifyWidget />
        </div>
      </div>
      <div className="widgets" style={{ display: "grid" }}>
        <div id="weatherWidget" style={getStyle("weatherWidget")}>
          <CalendarWidget />
        </div>
      </div>
      <div className="widgets" style={{ display: "grid" }}>
        <div id="weatherWidget" style={getStyle("weatherWidget")}>
          <ClockWidget />
        </div>
      </div>
      <div className="widgets" style={{ display: "grid" }}>
        <div id="weatherWidget" style={getStyle("weatherWidget")}>
          <SystemWidget />
        </div>
      </div>
      <div className="widgets" style={{ display: "grid" }}>
        <div id="weatherWidget" style={getStyle("weatherWidget")}>
          <GmailWidget />
        </div>
      </div>
      <div className="widgets" style={{ display: "grid" }}>
        <div id="weatherWidget" style={getStyle("weatherWidget")}>
          <WebcamWidget />
        </div>
      </div>
    </div>
  );
}
