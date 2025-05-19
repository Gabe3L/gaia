import { useEffect, useState } from "react";
import styles from "./CalendarWidget.module.css";
import baseWidget from "./BaseWidget.module.css";

export default function CalendarWidget({ style }) {
  const [calendarData, setCalendarData] = useState({
    date: "",
    first_day: "",
    event_titles: "",
  });

  useEffect(() => {
    const socket = new WebSocket(
      `ws:/${window.location.hostname}:8000/ws/calendar`
    );

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        const { date = "", first_day = "", event_titles = "" } = data;

        if (date && first_day && event_titles) {
          setCalendarData({ date, first_day, event_titles });
        }
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
      <div className={styles.date}>{calendarData.date}</div>
      <div className={styles.firstDay}>{calendarData.first_day}</div>
      <div className={styles.eventTitles}>{calendarData.event_titles}</div>
    </div>
  );
}
