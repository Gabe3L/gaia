import { useState, useEffect } from "react";
import styles from "./SpotifyWidget.module.css";
import baseWidget from "./BaseWidget.module.css";

type SpotifyWidgetProps = {
  style?: React.CSSProperties;
};

type SpotifyData = {
  title: string;
  current_time: string;
  total_time: string;
  next_artist: string;
  next_title: string;
  album_name: string;
  artist: string;
  album_cover: string | null;
};

const DEFAULT_SPOTIFY_DATA: SpotifyData = {
  title: "No Playback",
  current_time: "0:00",
  total_time: "0:00",
  next_artist: "No Artist",
  next_title: "Queue Empty",
  album_name: "Unknown Album",
  artist: "Unknown Artist",
  album_cover: null,
};

export default function SpotifyWidget({ style }: SpotifyWidgetProps) {
  const [data, setData] = useState<SpotifyData>(DEFAULT_SPOTIFY_DATA);

  useEffect(() => {
    const socket = new WebSocket(
      `ws:/${window.location.hostname}:8000/ws/spotify`
    );

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        const title = data.title ?? DEFAULT_SPOTIFY_DATA.title;
        const current_time =
          data.current_time ?? DEFAULT_SPOTIFY_DATA.current_time;
        const total_time = data.total_time ?? DEFAULT_SPOTIFY_DATA.total_time;
        const next_artist =
          data.next_artist ?? DEFAULT_SPOTIFY_DATA.next_artist;
        const next_title = data.next_title ?? DEFAULT_SPOTIFY_DATA.next_title;
        const album_name = data.album_name ?? DEFAULT_SPOTIFY_DATA.album_name;
        const artist = data.artist ?? DEFAULT_SPOTIFY_DATA.artist;
        const album_cover =
          data.album_cover ?? DEFAULT_SPOTIFY_DATA.album_cover;

        setData({
          title,
          current_time,
          total_time,
          next_artist,
          next_title,
          album_name,
          artist,
          album_cover,
        });
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
    const timeToSeconds = (str: string) => {
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
        {data.album_cover ? (
          <img
            className={styles.albumCover}
            src={data.album_cover}
            alt="Album Cover"
          />
        ) : (
          <div className={styles.noAlbumCover}>No Album Cover</div>
        )}
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
