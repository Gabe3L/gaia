import { useEffect, useRef } from 'react';

export default function WebcamWidget() {
  const videoRef = useRef(null);

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
        console.error(`Webcam error: ${err.message}`);
      }
    };

    startWebcam();

    return () => {
      const stream = videoRef.current?.srcObject;
      if (stream) {
        stream.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  return <video className="widget" id="webcam" ref={videoRef} autoPlay muted />;
}
