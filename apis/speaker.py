class Speaker:
    def __init__(self, speech_queue):
        self.tts = speech_queue

    def speak(self, message: str):
        print(f"[Gaia]: {message}")
        if message:
            self.tts.put(message)