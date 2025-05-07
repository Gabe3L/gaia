import os

from backend.app.apis.handlers.weather_handler import WeatherHandler
from backend.app.apis.handlers.joke_handler import JokeHandler
from backend.app.apis.handlers.music_handler import MusicHandler
from backend.app.apis.handlers.note_handler import NoteHandler
from backend.app.apis.handlers.date_time_handler import DateTimeHandler
from backend.app.apis.handlers.youtube_handler import YouTubeHandler
from backend.logs.logging_setup import setup_logger

class CommandRouter:
    def __init__(self, tts_queue):
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        self.logger = setup_logger(file_name)
        self.tts_queue = tts_queue
        self.intent_map = {
            "weather": WeatherHandler(),
            "joke": JokeHandler(),
            "music": MusicHandler(),
            "note": NoteHandler(),
            "date": DateTimeHandler("date"),
            "time": DateTimeHandler("time"),
            "youtube": YouTubeHandler(),
        }

    def route(self, label: str, elements: dict):
        """Takes the speech input as text from the user and converts it into a task"""
        try:
            handler = self.intent_map.get(label)
            if handler:
                self.logger.info(f'Routing {elements} to {handler.__class__.__name__}')
                handler.handle(self.tts_queue, elements)
        except Exception as e:
            self.logger.error(f'Error with routing: {e}')