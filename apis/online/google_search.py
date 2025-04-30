import os
import webbrowser
from queue import Queue

from logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

def google_search(command: str, speech_queue: Queue):
    search_url = f"https://www.google.com/search?q={command.replace(' ', '+')}"
    
    speech_queue.put("Okay! Searching Google.")
    speech_queue.put(f"Searching for: {command}")

    try:
        webbrowser.open(search_url)
    except Exception as e:
        speech_queue.put(f"An error occurred while trying to open the browser: {str(e)}")