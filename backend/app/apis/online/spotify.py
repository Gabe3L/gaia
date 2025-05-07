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
        with open("admin/spotify_creds.json", "r") as creds:
            credentials = json.load(creds)
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


##################################################

if __name__ == "__main__":
    spotify = Spotify()
    device_id = spotify.get_device_id()
    track_info = spotify.search_spotify(artist="AC/DC", song="Thunderstruck", genre="Rock")
    spotify.play_track(track_info['uri'], device_id)