import os
import json
import requests
from typing import Optional

from logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

def get_articles() -> Optional[str]:
    with open('config.json', 'r') as file:
        config = json.load(file)
        api_key = config.get("news_api_key")

    if not api_key:
        print("API key not found in config.json")
        return None
    
    url = f'https://newsapi.org/v2/everything?q=Canada&sortBy=popularity&apiKey={api_key}'
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        news_dict = response.json()
        return news_dict.get('articles', [])
    except Exception as e:
        print(f"Error fetching news: {e}")
        return None