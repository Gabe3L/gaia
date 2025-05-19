import { useEffect, useState } from "react";

export default function ClockWidget() {
  const [clockData, setClockData] = useState({
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
          setClockData({ time, date });
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
    <div className="widget" id="clock">
      <div className="time">{clockData.time}</div>
      <div className="date">{clockData.date}</div>
    </div>
  );
}
