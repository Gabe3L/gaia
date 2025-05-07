import os
import datetime
from typing import Optional

from logs.logging_setup import setup_logger

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