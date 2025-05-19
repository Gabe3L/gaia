export default function SpotifyWidget() {
  return (
    <div className="widget" id="spotify">
      <div className="box white">
        <div className="title">No Playback</div>
        <div className="time-container">
          <span className="current-time">0:00</span>
          <span className="total-time">0:00</span>
        </div>
        <div className="playback-bar">
          <div className="playback-fill" style={{ width: "0%" }}></div>
        </div>
      </div>
      <div className="box black">
        <img className="album-cover" src="" alt="Album Cover" />
      </div>
      <div className="box black">
        <div className="next-title">Queue Empty</div>
        <div className="next-artist">No Artist</div>
      </div>
      <div className="box white">
        <div className="album-name">Unknown Album</div>
        <div className="artist">Unknown Artist</div>
      </div>
    </div>
  );
}
