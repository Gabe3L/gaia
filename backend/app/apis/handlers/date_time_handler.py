from apis.offline import date_time

class DateTimeHandler:
    def __init__(self, mode):
        self.mode = mode

    def handle(self, user_command: dict, speaker):
        if self.mode == "date":
            speaker.speak(f"Today is {date_time.date()}")
        elif self.mode == "time":
            speaker.speak(f"The time is {date_time.time()}")