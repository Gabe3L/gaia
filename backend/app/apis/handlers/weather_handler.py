from apis.online import weather

class WeatherHandler:
    def handle(self, user_command: dict, speaker):
        city = user_command.get("city")
        forecast = weather.fetch_weather(city)
        speaker.speak(forecast)