import os
import time
import json
from typing import Optional, Dict, Any

import spotipy

from backend.logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################


class Spotify:
    def __init__(self) -> None:
        self.load_config()
        self.sp = spotipy.Spotify(
            auth_manager=spotipy.oauth2.SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope=self.scope,
            )
        )

    def load_config(self) -> None:
        base_dir = os.path.dirname(os.path.abspath(__file__))

        creds_path = os.path.join(
            base_dir, "..", "..", "..", "..", "shared", "admin", "spotify_creds.json")

        try:
            with open(creds_path, "r") as creds:
                credentials = json.load(creds)
        except FileNotFoundError:
            logger.error(f"Missing Spotify credentials file at {creds_path}")
            raise FileNotFoundError(f"Expected credentials at: {creds_path}")

        self.client_id = credentials["client_id"]
        self.client_secret = credentials["client_secret"]
        self.redirect_uri = credentials["redirect_uri"]
        self.scope = credentials["scope"]
        self.spotify_path = credentials["spotify_path"]

    def get_device_id(self) -> Optional[str]:
        try:
            start_time = time.time()
            while time.time() - start_time < 5:
                devices = self.sp.devices()
                if devices["devices"]:
                    for device in devices["devices"]:
                        if device["type"] == "Computer":
                            return device["id"]
                time.sleep(1)
        except Exception as e:
            logger.error("No computer device found within 5 seconds.")
            return None

    def search_spotify(self, **elements) -> Optional[Dict[str, Any]]:
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

        results = self.sp.search(q=query, type="track", limit=5)
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

    def play_track(self, track_uri: str, device_id: str) -> None:
        self.sp.start_playback(device_id=device_id, uris=[track_uri])

    def get_current_artist(self) -> Optional[str]:
        try:
            playback = self.sp.current_playback()
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

    def get_current_title(self) -> Optional[str]:
        try:
            playback = self.sp.current_playback()
            if playback:
                track = playback['item']
                return track.get('name')
            else:
                logger.info("No track is currently playing.")
                return None
        except Exception as e:
            logger.error(f"Error retrieving current track title: {e}")
            return None

    def get_current_timestamp(self) -> Optional[str]:
        try:
            playback = self.sp.current_playback()
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

    def get_current_total_duration(self) -> Optional[str]:
        try:
            playback = self.sp.current_playback()
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

    def get_current_album_name(self) -> Optional[str]:
        try:
            playback = self.sp.current_playback()
            if playback:
                album_name = playback['item']['album'].get('name')
                return album_name
            else:
                logger.info("No track is currently playing.")
                return None
        except Exception as e:
            logger.error(f"Error retrieving album name: {e}")
            return None

    def get_current_album_cover(self) -> Optional[str]:
        try:
            import requests

            playback = self.sp.current_playback()
            if playback:
                images = playback['item']['album'].get('images', [])
                if images:
                    return images[1].get('url')
                else:
                    logger.info("No album images found.")
            else:
                logger.info("No track is currently playing.")
        except Exception as e:
            logger.error(f"Error displaying album cover: {e}")

    def get_next_artist(self) -> Optional[str]:
        try:
            queue = self.sp.queue()
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

    def get_next_title(self) -> Optional[str]:
        try:
            queue = self.sp.queue()
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
    spotify = Spotify()
    device_id = spotify.get_device_id()
    track_info = spotify.search_spotify(
        artist="AC/DC", song="Thunderstruck", genre="Rock")
    spotify.play_track(track_info['uri'], device_id)
