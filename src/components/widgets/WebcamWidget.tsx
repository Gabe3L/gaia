import { useEffect, useRef } from 'react';
import styles from "./WebcamWidget.module.css";
import baseWidget from "./BaseWidget.module.css";

type WebcamWidgetProps = {
  style?: React.CSSProperties;
};

export default function WebcamWidget({ style }: WebcamWidgetProps) {
  const videoRef = useRef<HTMLVideoElement | null>(null);

  useEffect(() => {
    const startWebcam = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: false,
        });

        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
      } catch (err) {
        console.error(`Webcam error: ${err}`);
      }
    };

    startWebcam();

    return () => {
      const videoElement = videoRef.current;
      if (videoElement && videoElement.srcObject) {
        const stream = videoElement.srcObject as MediaStream;
        stream.getTracks().forEach(track => track.stop());
        videoElement.srcObject = null;
      }
    };
  }, []);

  return <video className={`${styles.webcam} ${baseWidget.widget}`} style={style} ref={videoRef} autoPlay muted />;
}
