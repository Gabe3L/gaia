import os
import webbrowser
from urllib import parse

from logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

def search_youtube(command: str) -> None:
    try:
        search_query = parse.urlencode({"search_query": command})
        search_url = f"http://www.youtube.com/results?{search_query}"
        webbrowser.open(search_url)

    except Exception as e:
        logger.error(f"Error: {e}")
        return None
    
if __name__ == "__main__":
    search_youtube("Testing Testing 123")