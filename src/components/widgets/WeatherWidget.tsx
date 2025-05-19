import { useState, useEffect } from "react";
import styles from './WeatherWidget.module.css';
import baseWidget from './BaseWidget.module.css';

type WeatherWidgetProps = {
  style?: React.CSSProperties;
};

type WeatherData = {
  location: string;
  temperature: string;
  precipitation: string;
  description: string;
};

const DEFAULT_WEATHER_DATA: WeatherData = {
    location: "No Location",
    temperature: "",
    precipitation: "",
    description: "",
};

export default function WeatherWidget({ style }: WeatherWidgetProps) {
  const [data, setData] = useState<WeatherData>(DEFAULT_WEATHER_DATA);

  useEffect(() => {
    const socket = new WebSocket(
      `ws:/${window.location.hostname}:8000/ws/weather`
    );

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        const location = data.location ?? DEFAULT_WEATHER_DATA.location;
        const temperature = data.temperature ?? DEFAULT_WEATHER_DATA.temperature;
        const precipitation = data.precipitation ?? DEFAULT_WEATHER_DATA.precipitation;
        const description = data.description ?? DEFAULT_WEATHER_DATA.description;

        setData({ location, temperature, precipitation, description });
      } catch (err) {
        console.error("Invalid weather data received:", err);
      }
    };

    socket.onerror = (error) => {
      console.error("Weather WebSocket error:", error);
    };

    socket.onclose = () => {
      console.warn("Weather WebSocket closed.");
    };

    return () => socket.close();
  }, []);

  return (
    <div className={`${styles.weather} ${baseWidget.widget}`} style={style}>
      <div className={styles.location}>{data.location}</div>
      <div className={styles.temperature}>
        {data.temperature ? `${data.temperature} °C` : ""}
      </div>
      <div className={styles.precipitation}>
        {data.precipitation ? `${data.precipitation} %` : ""}
      </div>
      <div className={styles.description}>{data.description}</div>
    </div>
  );
}
