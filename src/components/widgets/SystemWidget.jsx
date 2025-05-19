import { useEffect, useState } from "react";
import styles from './SystemWidget.module.css';
import baseWidget from './BaseWidget.module.css';

export default function SystemWidget({ style }) {
  const [data, setData] = useState({
    cpu_usage: "",
    gpu_usage: "",
    ram_usage: "",
    disk_usage: "",
  });

  useEffect(() => {
    const socket = new WebSocket(
      `ws:/${window.location.hostname}:8000/ws/system`
    );

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        const {
          cpu_usage = "",
          gpu_usage = "",
          ram_usage = "",
          disk_usage = "",
        } = data;

        if (cpu_usage && gpu_usage && ram_usage && disk_usage) {
          setData({ cpu_usage, gpu_usage, ram_usage, disk_usage });
        }
      } catch (err) {
        console.error("Invalid system data received:", err);
      }
    };

    socket.onerror = (error) => {
      console.error("System WebSocket error:", error);
    };

    socket.onclose = () => {
      console.warn("System WebSocket closed.");
    };

    return () => socket.close();
  }, []);

  return (
    <div className={`${styles.system} ${baseWidget.widget}`} style={style}>
      <div className={styles.cpu}>CPU: {data.cpu_usage}</div>
      <div className={styles.gpu}>GPU: {data.gpu_usage}</div>
      <div className={styles.ram}>RAM: {data.ram_usage}</div>
      <div className={styles.disk}>Disk: {data.disk_usage}</div>
    </div>
  );
}
