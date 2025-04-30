from apis.online import spotify

class MusicHandler:
    def handle(self, user_command: dict, speaker):
        speaker.speak("Playing music.")
        spotify.Spotify("play music")