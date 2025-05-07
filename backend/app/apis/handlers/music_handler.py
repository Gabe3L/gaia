import os
import json
from typing import Dict
from queue import Queue

from backend.logs.logging_setup import setup_logger
from backend.app.apis.online.spotify import Spotify
from backend.app.apis.offline.open_app import OpenApp

class MusicHandler:
    def __init__(self):
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        self.logger = setup_logger(file_name)
        self.spotify = Spotify()
        self.apple_music = None
        self.youtube_music = None
        self.amazon_music = None

    def handle(self, speech_queue: Queue, elements: Dict[str, str]):
        self.logger.info(f'Recieved: {elements}')
        
        requested_app = elements.get("app")
        app: str = None
        if requested_app:
            match requested_app.lower():
                case "spotify" | "spot":
                    app = "spotify"
                case "amazon" | "amazon music":
                    app = "amazon"
                case "you" | "tube" | "youtube" | "youtube music":
                    app = "youtube"
                case "apple" | "apple music":
                    app = "apple"
                case _:
                    self.logger.info(f'Unrecognized app "{requested_app}", using default.')
        else:
            self.logger.info(f'User didn\'t provide an app, using default.')
                   
        if app is None: 
            with open("config/preferences.json", "r") as f:
                preferences = json.load(f)
            app = preferences.get("music_app", "spotify").lower()
        
        self.logger.info(f"Streaming music from {app}")
        if app == "spotify":
            if not OpenApp.is_app_open(app):
                OpenApp.open_app(app)
            
            device_id = self.spotify.get_device_id()
            self.logger.info(f'Searching for {elements} on Spotify')
            track_info = self.spotify.search_spotify(**elements)
            self.spotify.play_track(track_info["uri"], device_id)
            speech_queue.put("Playing music.")