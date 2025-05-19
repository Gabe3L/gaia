export default function WeatherWidget() {
  return (
    <div className="widget" id="weather" data-location="" data-temperature="" data-precipitation="" data-description="">
      <div className="location">No Location</div>
      <div className="temperature"></div>
      <div className="precipitation"></div>
      <div className="description"></div>
    </div>
  );
}
