import { useEffect, useState } from "react";

export default function CalendarWidget() {
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
        console.error("Invalid calendar data received:", err);
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
    <div className="widget" id="calendar">
      <div className="date">{calendarData.date}</div>
      <div className="first-day">{calendarData.first_day}</div>
      <div className="event-titles">{calendarData.event_titles}</div>
    </div>
  );
}
