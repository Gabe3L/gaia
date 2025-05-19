import { useEffect, useState } from "react";
import styles from "./GmailWidget.module.css";
import baseWidget from "./BaseWidget.module.css";

type GmailWidgetProps = {
  style?: React.CSSProperties;
};

type GmailData = {
  senders: Array<string>;
  headers: Array<string>;
}

const DEFAULT_GMAIL_DATA: GmailData = {
  senders: ["Good Job :)"],
  headers: ["No Unread Emails!"],
};

export default function GmailWidget({ style }: GmailWidgetProps) {
  const [data, setData] = useState<GmailData>(DEFAULT_GMAIL_DATA);

  useEffect(() => {
    const socket = new WebSocket(
      `ws://${window.location.hostname}:8000/ws/gmail`
    );

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        
        const senders = data.senders ?? DEFAULT_GMAIL_DATA.senders;
        const headers = data.headers ?? DEFAULT_GMAIL_DATA.headers;

        setData({ senders, headers });
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
      <div className={styles.senders}>{data.senders}</div>
      <div className={styles.headers}>{data.headers}</div>
    </div>
  );
}
