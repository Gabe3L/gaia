import { useEffect, useState } from "react";
import styles from "./ClockWidget.module.css";
import baseWidget from "./BaseWidget.module.css";

type ClockWidgetProps = {
  style?: React.CSSProperties;
};

type ClockData = {
  time: string;
  date: string;
};

const DEFAULT_CLOCK_DATA: ClockData = {
  time: "00:00",
  date: "Date Unknown",
};

export default function ClockWidget({ style }: ClockWidgetProps) {
  const [data, setData] = useState<ClockData>(DEFAULT_CLOCK_DATA);

  useEffect(() => {
    const socket = new WebSocket(
      `ws:/${window.location.hostname}:8000/ws/clock`
    );

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        const time = data.time ?? DEFAULT_CLOCK_DATA.time;
        const date = data.date ?? DEFAULT_CLOCK_DATA.date;

        setData({ time, date });
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
