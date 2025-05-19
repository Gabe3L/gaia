import { useState, useEffect } from "react";
import styles from './SpotifyWidget.module.css';
import baseWidget from './BaseWidget.module.css';

export default function SpotifyWidget({ style }) {
  const [data, setData] = useState({
    title: "No Playback",
    current_time: "0:00",
    total_time: "0:00",
    next_artist: "No Artist",
    next_title: "Queue Empty",
    album_name: "Unknown Album",
    artist: "Unknown Artist",
    album_cover: null,
  });

  useEffect(() => {
    const socket = new WebSocket(
      `ws:/${window.location.hostname}:8000/ws/spotify`
    );

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        const mergedData = {
          title: data.title || "No Playback",
          current_time: data.current_time || "0:00",
          total_time: data.total_time || "0:00",
          next_artist: data.next_artist || "No Artist",
          next_title: data.next_title || "Queue Empty",
          album_name: data.album_name || "Unknown Album",
          artist: data.artist || "Unknown Artist",
          album_cover: data.album_cover || null,
        };

        setData(mergedData);
      } catch (err) {
        console.error("Invalid JSON data:", err);
      }
    };

    socket.onerror = (err) => {
      console.error("Spotify WebSocket Error:", err);
    };

    socket.onclose = () => {
      console.warn("Spotify WebSocket closed.");
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
    <div className={`${styles.spotify} ${baseWidget.widget}`} style={style}>
      <div className={`${styles.box} ${styles.white}`}>
        <div className={styles.title}>{data.title}</div>
        <div className={styles.timeContainer}>
          <span className={styles.currentTime}>{data.current_time}</span>
          <span className={styles.totalTime}>{data.total_time}</span>
        </div>
        <div className={styles.playbackBar}>
          <div
            className={styles.playbackFill}
            style={{ width: `${getProgressPercent()}%` }}
          ></div>
        </div>
      </div>

      <div className={`${styles.box} ${styles.black}`}>
        <img className={styles.albumCover} src={data.album_cover} alt="Album Cover" />
      </div>

      <div className={`${styles.box} ${styles.black}`}>
        <div className={styles.nextTitle}>{data.next_title}</div>
        <div className={styles.nextArtist}>{data.next_artist}</div>
      </div>

      <div className={`${styles.box} ${styles.white}`}>
        <div className={styles.albumName}>{data.album_name}</div>
        <div className={styles.artist}>{data.artist}</div>
      </div>
    </div>
  );
}
