import os
import datetime
from logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

def date() -> str | bool:
    try:
        return datetime.datetime.now().strftime("%b %d %Y")
    except Exception as e:
        logger.error(e)
        return False

def time() -> str | bool:
    try:
        return datetime.datetime.now().strftime("%H:%M:%S")
    except Exception as e:
        logger.error(e)
        return False