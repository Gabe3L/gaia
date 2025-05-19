import { useState, useEffect } from "react";
import styles from './WeatherWidget.module.css';
import baseWidget from './BaseWidget.module.css';

export default function WeatherWidget({ style }) {
  const [data, setData] = useState({
    location: "No Location",
    temperature: "",
    precipitation: "",
    description: "",
  });

  useEffect(() => {
    const socket = new WebSocket(
      `ws:/${window.location.hostname}:8000/ws/weather`
    );

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        const {
          location = "No Location",
          temperature = "",
          precipitation = "",
          description = "",
        } = data;

        if (location && temperature && precipitation && description) {
          setData({ location, temperature, precipitation, description });
        }
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
