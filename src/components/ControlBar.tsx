import { useState } from "react";
import styles from './ControlBar.module.css'

const initialThreadStates = {
  camera: false,
  speech_to_text: false,
  text_to_speech: false,
  performing_actions: false,
};

type ThreadName = keyof typeof initialThreadStates;

export default function ControlBar() {
  const [threadStates, setThreadStates] = useState<typeof initialThreadStates>(initialThreadStates);

  function toggleThread(name: ThreadName) {
    if (!(name in threadStates)) {
      console.error(`Unknown thread: ${name}`);
      return;
    }

    const isRunning = threadStates[name];
    const endpoint = isRunning ? `/stop-thread/${name}` : `/start-thread/${name}`;

    fetch(endpoint, { method: "POST" })
      .then((response) => {
        if (!response.ok) throw new Error(`Server returned ${response.status}`);
        return response.json();
      })
      .then((data) => {
        setThreadStates((prevStates) => ({
          ...prevStates,
          [name]: !isRunning,
        }));
        const action = isRunning ? "Stopped" : "Started";
        console.info(`${action} ${name} thread.`);
        console.info(data);
      })
      .catch((err) => {
        console.error(`Error toggling ${name}: ${err.message}`);
      });
  }

  return (
    <div className={styles.controlBar}>
      <button id="menu-button">🪟</button>
      <div className={styles.controlButtons}>
        <button
          onClick={() => toggleThread("camera")}
          style={{ backgroundColor: threadStates.camera ? "green" : "red" }}
          title={threadStates.camera ? "Stop Camera" : "Start Camera"}
        >
          🎥
        </button>
        <button
          onClick={() => toggleThread("speech_to_text")}
          style={{ backgroundColor: threadStates.speech_to_text ? "green" : "red" }}
          title={threadStates.speech_to_text ? "Stop Speech to Text" : "Start Speech to Text"}
        >
          🎤
        </button>
        <button
          onClick={() => toggleThread("text_to_speech")}
          style={{ backgroundColor: threadStates.text_to_speech ? "green" : "red" }}
          title={threadStates.text_to_speech ? "Stop Text to Speech" : "Start Text to Speech"}
        >
          🔊
        </button>
      </div>
      <button id="transcription-button">📜</button>
    </div>
  );
}
