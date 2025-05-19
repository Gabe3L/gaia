import { useState, useEffect } from "react";

export default function WeatherWidget() {
  const [weather, setWeather] = useState({
    location: "No Location",
    temperature: "",
    precipitation: "",
    description: "",
  });

  useEffect(() => {
    const socket = new WebSocket(
      `ws:/${window.location.hostname}:8000/ws/weather`
    );

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        const {
          location = "No Location",
          temperature = "",
          precipitation = "",
          description = "",
        } = data;

        if (location && temperature && precipitation && description) {
          setWeather({ location, temperature, precipitation, description });
        }
      } catch (err) {
        console.error("Invalid weather data received:", err);
      }
    };

    socket.onerror = (error) => {
      console.error("Weather WebSocket error:", error);
    };

    socket.onclose = () => {
      console.warn("Weather WebSocket closed.");
    };

    return () => socket.close();
  }, []);

  return (
    <div className="widget" id="weather">
      <div className="location">{weather.location}</div>
      <div className="temperature">
        {weather.temperature ? `${weather.temperature} °C` : ""}
      </div>
      <div className="precipitation">
        {weather.precipitation ? `${weather.precipitation} %` : ""}
      </div>
      <div className="description">{weather.description}</div>
    </div>
  );
}
