from backend.app.apis.online import youtube

class YouTubeHandler:
    def handle(self, user_command: dict, speaker):
        query = user_command.get("query")
        youtube.search_youtube(query)
        speaker.speak(f"Searching YouTube for {query}.")