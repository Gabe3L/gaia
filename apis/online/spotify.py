import os
import time
import json
import subprocess
from typing import Optional

import spotipy

from logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

class Spotify:
    def __init__(self, request) -> None:
        self.load_config()
        self.sp = spotipy.Spotify(auth_manager=spotipy.oauth2.SpotifyOAuth(client_id=self.client_id,
                                                    client_secret=self.client_secret,
                                                    redirect_uri=self.redirect_uri,
                                                    scope=self.scope))
        self.find_and_play_song(request)

    def find_and_play_song(self, song: str) -> None:
        self.launch_spotify()
        device_id = self.get_device_id()
        track_uri = self.search_track(song)
        self.play_track(track_uri, device_id)

    def load_config(self) -> None:
        with open("admin/spotify_creds.json", "r") as creds:
            credentials = json.load(creds)
        self.client_id = credentials['client_id']
        self.client_secret = credentials['client_secret']
        self.redirect_uri = credentials['redirect_uri']
        self.scope = credentials['scope']
        self.spotify_path = credentials['spotify_path']

    def launch_spotify(self) -> None:
        try:
            if not os.path.exists(self.spotify_path):
                raise FileNotFoundError("Spotify executable not found at the specified path.")
            
            subprocess.Popen([self.spotify_path])
        except Exception as e:
            raise Exception(f"Error launching Spotify: {e}")

    def get_device_id(self) -> Optional[str]:
        try:
            start_time = time.time()
            while time.time() - start_time < 5:
                devices = self.sp.devices()
                if devices['devices']:
                    for device in devices['devices']:
                        if device['type'] == 'Computer':
                            return device['id']
                time.sleep(1)
        except Exception as e:
            logger.error("No computer device found within 5 seconds.")
            return None

    def search_track(self, track_name:str) -> str:
        results = self.sp.search(q=track_name, type='track', limit=1)
        if not results['tracks']['items']:
            raise Exception("Track not found.")
        track = results['tracks']['items'][0]
        return track['uri']

    def play_track(self, track_uri: str, device_id: str) -> None:
        self.sp.start_playback(device_id=device_id, uris=[track_uri])

##################################################

if __name__ == "__main__":
    spotify = Spotify('Beethoven')