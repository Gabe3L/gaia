import { useEffect, useState } from "react";
import styles from "./GmailWidget.module.css";
import baseWidget from "./BaseWidget.module.css";

export default function GmailWidget({ style }) {
  const [senders, setSenders] = useState("Good Job :)");
  const [headers, setHeaders] = useState("No Unread Emails!");

  useEffect(() => {
    const socket = new WebSocket(
      `ws://${window.location.hostname}:8000/ws/gmail`
    );

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        const {
          senders: newSenders = "Good Job :)",
          headers: newHeaders = "No Unread Emails!",
        } = data;

        setSenders(newSenders);
        setHeaders(newHeaders);
      } catch (err) {
        console.error("Invalid JSON data:", err);
      }
    };

    socket.onerror = (error) => {
      console.error("Gmail WebSocket error:", error);
    };

    socket.onclose = () => {
      console.warn("Gmail WebSocket closed.");
    };

    return () => socket.close();
  }, []);

  return (
    <div className={`${styles.gmail} ${baseWidget.widget}`} style={style}>
      <div className={styles.senders}>{senders}</div>
      <div className={styles.headers}>{headers}</div>
    </div>
  );
}
