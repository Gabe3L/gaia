import webbrowser
from queue import Queue

def google_search(command: str, tts_queue: Queue):
    search_url = f"https://www.google.com/search?q={command.replace(' ', '+')}"
    
    tts_queue.put("Okay! Searching Google.")
    tts_queue.put(f"Searching for: {command}")

    try:
        webbrowser.open(search_url)
    except Exception as e:
        tts_queue.put(f"An error occurred while trying to open the browser: {str(e)}")