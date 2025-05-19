import { useState, useEffect } from "react";

export default function SpotifyWidget() {
  const [data, setData] = useState({
    title: "No Playback",
    current_time: "0:00",
    total_time: "0:00",
    next_artist: "No Artist",
    next_title: "Queue Empty",
    album_name: "Unknown Album",
    artist: "Unknown Artist",
    album_cover: "",
  });

  useEffect(() => {
    const socket = new WebSocket(
      `ws:/${window.location.hostname}:8000/ws/spotify`
    );

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log("Received:", data);

        const mergedData = {
          title: data.title || "No Playback",
          current_time: data.current_time || "0:00",
          total_time: data.total_time || "0:00",
          next_artist: data.next_artist || "No Artist",
          next_title: data.next_title || "Queue Empty",
          album_name: data.album_name || "Unknown Album",
          artist: data.artist || "Unknown Artist",
          album_cover: data.album_cover || "",
        };

        setData(mergedData);
      } catch (err) {
        console.error("Invalid JSON data:", err);
      }
    };

    socket.onerror = (err) => {
      console.error("WebSocket Error:", err);
    };

    socket.onclose = () => {
      console.warn("WebSocket closed.");
    };

    return () => socket.close();
  }, []);

  const getProgressPercent = () => {
    const timeToSeconds = (str) => {
      const [min, sec] = str.split(":").map(Number);
      return min * 60 + sec || 0;
    };
    const current = timeToSeconds(data.current_time);
    const total = timeToSeconds(data.total_time);
    return total > 0 ? Math.min((current / total) * 100, 100) : 0;
  };

  return (
    <div className="widget" id="spotify">
      <div className="box white">
        <div className="title">{data.title}</div>
        <div className="time-container">
          <span className="current-time">{data.current_time}</span>
          <span className="total-time">{data.total_time}</span>
        </div>
        <div className="playback-bar">
          <div
            className="playback-fill"
            style={{ width: `${getProgressPercent()}%` }}
          ></div>
        </div>
      </div>
      <div className="box black">
        <img className="album-cover" src={data.album_cover} alt="Album Cover" />
      </div>
      <div className="box black">
        <div className="next-title">{data.next_title}</div>
        <div className="next-artist">{data.next_artist}</div>
      </div>
      <div className="box white">
        <div className="album-name">{data.album_name}</div>
        <div className="artist">{data.artist}</div>
      </div>
    </div>
  );
}
