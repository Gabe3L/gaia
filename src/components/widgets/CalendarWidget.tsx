import { useEffect, useState } from "react";
import styles from "./CalendarWidget.module.css";
import baseWidget from "./BaseWidget.module.css";

type CalendarWidgetProps = {
  style?: React.CSSProperties;
};

type CalendarData = {
  date: string;
  first_day: string;
  event_titles: string;
};

const DEFAULT_CALENDAR_DATA: CalendarData = {
  date: "",
  first_day: "",
  event_titles: "",
};

export default function CalendarWidget({ style }: CalendarWidgetProps) {
  const [data, setData] = useState<CalendarData>(DEFAULT_CALENDAR_DATA);

  useEffect(() => {
    const socket = new WebSocket(
      `ws:/${window.location.hostname}:8000/ws/calendar`
    );

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        const date = data.date ?? DEFAULT_CALENDAR_DATA.date;
        const first_day = data.first_day ?? DEFAULT_CALENDAR_DATA.first_day;
        const event_titles = data.event_titles ?? DEFAULT_CALENDAR_DATA.event_titles;

        setData({ date, first_day, event_titles });
      } catch (err) {
        console.error("Invalid cal endar data received:", err);
      }
    };

    socket.onerror = (error) => {
      console.error("Calendar WebSocket error:", error);
    };

    socket.onclose = () => {
      console.warn("Calendar WebSocket closed.");
    };

    return () => socket.close();
  }, []);

  return (
    <div className={`${styles.calendar} ${baseWidget.widget}`} style={style}>
      <div className={styles.date}>{data.date}</div>
      <div className={styles.firstDay}>{data.first_day}</div>
      <div className={styles.eventTitles}>{data.event_titles}</div>
    </div>
  );
}
