import { useEffect, useState } from "react";
import styles from "./ClockWidget.module.css";
import baseWidget from "./BaseWidget.module.css";

export default function ClockWidget({ style }) {
  const [data, setData] = useState({
    time: "00:00",
    date: "Date Unknown",
  });

  useEffect(() => {
    const socket = new WebSocket(
      `ws:/${window.location.hostname}:8000/ws/clock`
    );

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        const { time = "00:00", date = "Date Unknown" } = data;

        if (time && date) {
          setData({ time, date });
        }
      } catch (err) {
        console.error("Invalid clock data received:", err);
      }
    };

    socket.onerror = (error) => {
      console.error("Clock WebSocket error:", error);
    };

    socket.onclose = () => {
      console.warn("Clock WebSocket closed.");
    };

    return () => socket.close();
  }, []);

  return (
    <div className={`${styles.clock} ${baseWidget.widget}`} style={style}>
      <div className={styles.time}>{data.time}</div>
      <div className={styles.date}>{data.date}</div>
    </div>
  );
}
