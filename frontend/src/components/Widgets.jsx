import WeatherWidget from './widgets/WeatherWidget';
import SpotifyWidget from './widgets/SpotifyWidget';
import CalendarWidget from './widgets/CalendarWidget';
import ClockWidget from './widgets/ClockWidget';
import SystemWidget from './widgets/SystemWidget';
import GmailWidget from './widgets/GmailWidget';
import WebcamWidget from './widgets/WebcamWidget';

export default function Widgets() {
  return (
    <div className="widgets">
      <WeatherWidget />
      <SpotifyWidget />
      <CalendarWidget />
      <ClockWidget />
      <SystemWidget />
      <GmailWidget />
      <WebcamWidget />
    </div>
  );
}
