import os
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

################################################################

if __name__ == "__main__":
    print(get_month()) # %b 