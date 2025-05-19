import { useEffect, useState } from "react";

export default function SystemWidget() {
  const [systemData, setSystemData] = useState({
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
          setSystemData({ cpu_usage, gpu_usage, ram_usage, disk_usage });
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

    return () => socket.close(); // Cleanup
  }, []);

  return (
    <div className="widget" id="system">
      <div className="cpu">CPU: {systemData.cpu_usage}</div>
      <div className="gpu">GPU: {systemData.gpu_usage}</div>
      <div className="ram">RAM: {systemData.ram_usage}</div>
      <div className="disk">Disk: {systemData.disk_usage}</div>
    </div>
  );
}
