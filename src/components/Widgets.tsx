import { useState, useEffect } from "react";
import styles from "./Widgets.module.css";

import WeatherWidget from "./widgets/WeatherWidget";
import SpotifyWidget from "./widgets/SpotifyWidget";
import CalendarWidget from "./widgets/CalendarWidget";
import ClockWidget from "./widgets/ClockWidget";
import SystemWidget from "./widgets/SystemWidget";
import GmailWidget from "./widgets/GmailWidget";

type WidgetId =
  | "weather"
  | "spotify"
  | "calendar"
  | "clock"
  | "system"
  | "email";

type WidgetConfigEntry = {
  visible: boolean;
  gridWidth: number;
  gridHeight: number;
  xLocation: number;
  yLocation: number;
};

type WidgetConfig = {
  [key in WidgetId]: WidgetConfigEntry;
};

export default function Widgets() {
  const [widgetConfig, setWidgetConfig] = useState<Partial<WidgetConfig>>({});

  useEffect(() => {
    fetch("/settings/widgets.json")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Failed to fetch widget config");
        }
        return response.json();
      })
      .then((data) => {
      if (data.widgets) setWidgetConfig(data.widgets);
      })
      .catch((error) => {
        console.error("Error loading widget config:", error);
      });
  }, []);

  const getStyle = (id: WidgetId): React.CSSProperties => {
    const config = widgetConfig[id];
    if (
      !config ||
      !config.visible ||
      config.gridWidth == null ||
      config.gridHeight == null ||
      config.xLocation == null ||
      config.yLocation == null
    ) {
      return { display: "none" };
    }

    const { gridWidth, gridHeight, xLocation, yLocation } = config;

    return {
      gridColumnStart: xLocation + 1,
      gridColumnEnd: `span ${gridWidth}`,
      gridRowStart: yLocation + 1,
      gridRowEnd: `span ${gridHeight}`,
    };
  };

return (
    <div className={styles.widgets}>
      <WeatherWidget style={getStyle("weather")} />
      <SpotifyWidget style={getStyle("spotify")} />
      <CalendarWidget style={getStyle("calendar")} />
      <ClockWidget style={getStyle("clock")} />
      <SystemWidget style={getStyle("system")} />
      <GmailWidget style={getStyle("email")} />
    </div>
  );
}
