import pyjokes

class JokeHandler:
    def handle(self, user_command: dict, speaker):
        speaker.speak(pyjokes.get_joke())