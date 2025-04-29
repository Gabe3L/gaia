import sys
import time
import random
import datetime
import pyjokes
import pywhatkit
from queue import Queue
from typing import Optional

from features.online import *
from features.offline import *

############################################################################

GREETINGS = ["hello gaia", "gaia", "wake up gaia", "you there gaia", "time to work gaia", "hey gaia"]
GREETINGS_RES = ["always there for you sir", "I am ready sir", "your wish is my command", "how can I help you sir?", "I am online and ready sir"]
CALENDAR_STRS = ["what do i have", "do i have plans", "am i busy"]

############################################################################

class ActionManager():
    def __init__(self, tts_queue, request_queue):
        self.tts = tts_queue
        self.request = request_queue
    
    def welcome_user(self):
        self.tts.put("Initializing Gaia")
        time.sleep(1)
        hour = datetime.datetime.now().hour
        greet = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"
        self.tts.put(f'{greet} Gabe! Gaia is online and ready sir.')

    def execute_task(self, command, tts_queue: Queue):
        if not command:
            return None
        
        if "date" in command:
            self.tts.put(f'Today is {date_time.date()}')

        elif "time" in command:
            self.tts.put(f"Sir, the time is {date_time.time()}")

        elif "launch" in command:
            self.launch_application(command)

        elif command in GREETINGS:
            self.tts.put(random.choice(GREETINGS_RES))

        elif "open" in command:
            domain = command.split(' ')[-1]
            if open_website.open_website(domain):
                self.tts.put(f"Alright sir, opening {domain}")
            else:
                self.tts.put("Unable to open the website.")

        elif any(word in command for word in ["weather", "temperature"]):
            city = command.split(' ')[-1]
            self.tts.put(weather.fetch_weather(city=city))

        elif "tell me about" in command:
            topic = command.split('about ')[-1]
            self.tts.put(wikipedia.tell_me_about(topic) if topic else "Sorry sir. I couldn't find any information.")

        elif any(word in command for word in ["buzzing", "news", "headlines"]):
            articles: Optional[dict] = news.get_articles()
            self.tts.put('Today\'s Headlines are:')
            for index, article in enumerate(articles):
                self.tts.put(article)
                if index == len(articles) - 2:
                    break
            self.tts.put('These were the top headlines, Have a nice day, Sir!')

        elif "search google for" in command:
            google_search.google_search(command, tts_queue)

        elif any(word in command for word in ["play music", "hit some music"]):
            self.play_music()

        elif "youtube" in command:
            video = command.split('youtube ')[1]
            self.tts.put(f"Okay sir, playing {video} on YouTube")
            pywhatkit.playonyt(video)

        elif any(word in command for word in CALENDAR_STRS):
            google_calendar.get_events(command, tts_queue)

        elif any(word in command for word in ["make a note", "write this down", "remember this"]):
            note.write_note(command)

        elif "joke" in command:
            self.tts.put(pyjokes.get_joke())

        elif "system" in command:
            self.tts.put(system_stats.system_stats())

        elif "where is" in command:
            self.tts.put(location.distance_to_place(command))

        elif any(word in command for word in ["where am I", "current location", "where i am"]):
            self.tts.put(location.my_location())

        elif any(word in command for word in ["goodbye", "offline", "bye"]):
            self.tts.put("Alright sir, going offline. It was nice working with you.")
            sys.exit()