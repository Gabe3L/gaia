from apis.online.spotify import Spotify
from queue import Queue

class MusicHandler:
    def __init__(self):
        self.spotify = Spotify("play music")
        self.apple_music = None
        self.youtube_music = None
        self.amazon_music = None

    def handle(self, speech_queue: Queue, **kwargs):
        if kwargs.get("app") == "spotify":
            self.play_music(kwargs)
        speech_queue.put("Playing music.")