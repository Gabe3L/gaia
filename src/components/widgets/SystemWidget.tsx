import { useEffect, useState } from "react";
import styles from './SystemWidget.module.css';
import baseWidget from './BaseWidget.module.css';

type SystemWidgetProps = {
  style?: React.CSSProperties;
};

type SystemData = {
  cpu_usage: string,
  gpu_usage: string;
  ram_usage: string;
  disk_usage: string;
};

const DEFAULT_SYSTEM_DATA: SystemData = {
  cpu_usage: "",
  gpu_usage: "",
  ram_usage: "",
  disk_usage: "",
};

export default function SystemWidget({ style }: SystemWidgetProps) {
  const [data, setData] = useState<SystemData>(DEFAULT_SYSTEM_DATA);

  useEffect(() => {
    const socket = new WebSocket(
      `ws:/${window.location.hostname}:8000/ws/system`
    );

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        const cpu_usage = data.cpu_usage ?? DEFAULT_SYSTEM_DATA.cpu_usage;
        const gpu_usage = data.gpu_usage ?? DEFAULT_SYSTEM_DATA.gpu_usage;
        const ram_usage = data.ram_usage ?? DEFAULT_SYSTEM_DATA.ram_usage;
        const disk_usage = data.disk_usage ?? DEFAULT_SYSTEM_DATA.disk_usage;

        setData({ cpu_usage, gpu_usage, ram_usage, disk_usage });
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
