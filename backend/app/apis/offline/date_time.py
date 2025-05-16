import os
import json
import datetime
from typing import Optional

from backend.logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

def date() -> Optional[str]:
    try:
        return datetime.datetime.now().strftime("%b %d %Y")
    except Exception as e:
        logger.error(e)
        return None

def time() -> Optional[str]:
    try:
        return datetime.datetime.now().strftime("%H:%M:%S")
    except Exception as e:
        logger.error(e)
        return None

def get_hour() -> Optional[int]:
    try:
        return int(datetime.datetime.now().strftime("%H"))
    except Exception as e:
        logger.error(e)
        return None

def get_minute() -> Optional[int]:
    try:
        return int(datetime.datetime.now().strftime("%M"))
    except Exception as e:
        logger.error(e)
        return None

def get_day() -> Optional[str]:
    try:
        return datetime.datetime.now().strftime("%d")
    except Exception as e:
        logger.error(e)
        return None

def get_month() -> Optional[str]:
    try:
        return datetime.datetime.now().strftime("%b")
    except Exception as e:
        logger.error(e)
        return None

def get_year() -> Optional[str]:
    try:
        return datetime.datetime.now().strftime("%Y")
    except Exception as e:
        logger.error(e)
        return None

def get_formatted_date() -> Optional[str]:
    try:
        time = datetime.datetime.now()
        day = time.day

        if 10 <= day % 100 <= 20:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")

        formatted_date = time.strftime(f"%B {day}{suffix}, %Y")
        return formatted_date
    except Exception as e:
        logger.error(e)
        return None

def get_formatted_time() -> Optional[str]:
    try:
        now = datetime.datetime.now()
        hour = now.hour
        minute = now.minute

        with open("shared/settings/preferences.json", "r") as file:
            settings = json.load(file)

        if settings.get("use_24_hour_time"):
            formatted_time = f"{hour}:{minute}"
        else:
            suffix = "AM" if hour < 12 else "PM"
            hour_12 = hour % 12 or 12
            formatted_time = f"{hour_12}:{minute} {suffix}"

        return formatted_time
    except Exception as e:
        logger.error(e)
        return None

################################################################

if __name__ == "__main__":
    print(get_formatted_time()) # %b 