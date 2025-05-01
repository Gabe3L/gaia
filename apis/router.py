import os

from apis.handlers.weather_handler import WeatherHandler
from apis.handlers.joke_handler import JokeHandler
from apis.handlers.music_handler import MusicHandler
from apis.handlers.note_handler import NoteHandler
from apis.handlers.date_time_handler import DateTimeHandler
from apis.handlers.youtube_handler import YouTubeHandler
from logs.logging_setup import setup_logger

class CommandRouter:
    def __init__(self, assistant):
        file_name = os.path.splitext(os.path.basename(__file__))[0]
        self.logger = setup_logger(file_name)

        self.assistant = assistant
        self.intent_map = {
            "get_weather": WeatherHandler(),
            "tell_joke": JokeHandler(),
            "play_music": MusicHandler(),
            "take_note": NoteHandler(),
            "get_date": DateTimeHandler("date"),
            "get_time": DateTimeHandler("time"),
            "youtube_search": YouTubeHandler(),
        }

    def route(self, user_command: str):
        """Takes the speech input as text from the user and converts it into a task"""
        handler = self.intent_map.get(user_command)
        if handler:
            handler.handle(user_command, self.assistant)
    
    def speak(self, message: str):
        if message:
            self.logger.info(f"[Gaia]: {message}")
            self.tts.put(message)