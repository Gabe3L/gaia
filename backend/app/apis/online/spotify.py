import os
import time
import json
from typing import Optional, Dict, Any

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

from backend.logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

_credentials = None
_sp_client = None

def load_config() -> Dict[str, Any]:
    global _credentials
    if _credentials is None:
        creds_path = os.path.join("backend", "app", "admin", "spotify_creds.json")
        try:
            with open(creds_path, "r") as creds:
                _credentials = json.load(creds)
        except FileNotFoundError:
            logger.error(f"Missing Spotify credentials file at {creds_path}")
            raise FileNotFoundError(f"Expected credentials at: {creds_path}")
    return _credentials

def get_spotify_client() -> Spotify:
    global _sp_client
    if _sp_client is None:
        creds = load_config()
        _sp_client = Spotify(
            auth_manager=SpotifyOAuth(
                client_id=creds["client_id"],
                client_secret=creds["client_secret"],
                redirect_uri=creds["redirect_uri"],
                scope=creds["scope"],
            )
        )
    return _sp_client

def get_device_id() -> Optional[str]:
    sp_client = get_spotify_client()
    try:
        start_time = time.time()
        while time.time() - start_time < 5:
            devices = sp_client.devices()
            if devices["devices"]:
                for device in devices["devices"]:
                    if device["type"] == "Computer":
                        return device["id"]
            time.sleep(1)
    except Exception:
        logger.error("No computer device found within 5 seconds.")
        return None

def search_spotify(**elements) -> Optional[Dict[str, Any]]:
    sp_client = get_spotify_client()

    query_parts = []

    if "artist" in elements:
        query_parts.append(f"artist:{elements['artist']}")
    if "song" in elements:
        query_parts.append(f"track:{elements['song']}")
    if "album" in elements:
        query_parts.append(f"album:{elements['album']}")
    if "genre" in elements:
        query_parts.append(f"genre:{elements['genre']}")

    query = " ".join(query_parts)
    if not query:
        raise Exception("No valid search parameters provided.")

    results = sp_client.search(q=query, type="track", limit=5)
    tracks = results.get("tracks", {}).get("items", [])
    if not tracks:
        raise Exception("No tracks found.")

    track = tracks[0]
    return {
        'name': track['name'],
        'artist': track['artists'][0]['name'],
        'album': track['album']['name'],
        'url': track['external_urls']['spotify'],
        'uri': track['uri']
    }

def play_track(track_uri: str, device_id: Optional[str] = None) -> None:
    sp_client = get_spotify_client()
    if device_id is None:
        device_id = get_device_id()
    if device_id is None:
        logger.error("No device found to play on.")
        return
    sp_client.start_playback(device_id=device_id, uris=[track_uri])

def get_current_artist() -> Optional[str]:
    sp_client = get_spotify_client()
    try:
        playback = sp_client.current_playback()
        if playback:
            artists = playback['item']['artists']
            if artists:
                artist_names = [artist['name'] for artist in artists]
                return ", ".join(artist_names)
        else:
            logger.info("No track is currently playing.")
            return None
    except Exception as e:
        logger.error(f"Error retrieving current artist: {e}")
        return None

def get_current_title() -> Optional[str]:
    sp_client = get_spotify_client()
    try:
        playback = sp_client.current_playback()
        if playback:
            track = playback['item']
            return track.get('name')
        else:
            logger.info("No track is currently playing.")
            return None
    except Exception as e:
        logger.error(f"Error retrieving current track title: {e}")
        return None

def get_current_timestamp() -> Optional[str]:
    sp_client = get_spotify_client()
    try:
        playback = sp_client.current_playback()
        if playback:
            progress_ms = playback.get('progress_ms', 0)
            minutes = progress_ms // 60000
            seconds = (progress_ms % 60000) // 1000
            return f"{minutes}:{seconds:02d}"
        else:
            logger.info("No track is currently playing.")
            return None
    except Exception as e:
        logger.error(f"Error retrieving current timestamp: {e}")
        return None

def get_current_total_duration() -> Optional[str]:
    sp_client = get_spotify_client()
    try:
        playback = sp_client.current_playback()
        if playback:
            duration_ms = playback['item'].get('duration_ms', 0)
            minutes = duration_ms // 60000
            seconds = (duration_ms % 60000) // 1000
            return f"{minutes}:{seconds:02d}"
        else:
            logger.info("No track is currently playing.")
            return None
    except Exception as e:
        logger.error(f"Error retrieving track duration: {e}")
        return None

def get_current_album_name() -> Optional[str]:
    sp_client = get_spotify_client()
    try:
        playback = sp_client.current_playback()
        if playback:
            album_name = playback['item']['album'].get('name')
            return album_name
        else:
            logger.info("No track is currently playing.")
            return None
    except Exception as e:
        logger.error(f"Error retrieving album name: {e}")
        return None

def get_current_album_cover() -> Optional[str]:
    sp_client = get_spotify_client()
    try:
        playback = sp_client.current_playback()
        if playback:
            images = playback['item']['album'].get('images', [])
            if images:
                if len(images) > 1:
                    return images[1].get('url')
                else:
                    return images[0].get('url')
            else:
                logger.info("No album images found.")
        else:
            logger.info("No track is currently playing.")
    except Exception as e:
        logger.error(f"Error displaying album cover: {e}")

def get_next_artist() -> Optional[str]:
    sp_client = get_spotify_client()
    try:
        queue = sp_client.queue()
        next_tracks = queue.get("queue", [])
        if next_tracks:
            next_track = next_tracks[0]
            artists = next_track.get('artists', [])
            if artists:
                artist_names = [artist['name'] for artist in artists]
                return ", ".join(artist_names)
        logger.info("Queue is empty or no next track found.")
        return None
    except Exception as e:
        logger.error(f"Error retrieving next artist in queue: {e}")
        return None

def get_next_title() -> Optional[str]:
    sp_client = get_spotify_client()
    try:
        queue = sp_client.queue()
        next_tracks = queue.get("queue", [])
        if next_tracks:
            next_track = next_tracks[0]
            return next_track.get('name')
        logger.info("Queue is empty or no next track found.")
        return None
    except Exception as e:
        logger.error(f"Error retrieving next track title: {e}")
        return None

##################################################

if __name__ == "__main__":
    track_info = search_spotify(artist="AC/DC", song="Thunderstruck", genre="Rock")
    play_track(track_info['uri'])

    print(get_current_album_name())