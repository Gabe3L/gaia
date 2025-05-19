import { useEffect, useState } from "react";

export default function GmailWidget() {
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
        console.error("Invalid Gmail data:", err);
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
    <div className="widget" id="gmail">
      <div className="senders">{senders}</div>
      <div className="headers">{headers}</div>
    </div>
  );
}
