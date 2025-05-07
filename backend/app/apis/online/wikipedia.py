import os
from typing import Optional, Any

import wikipedia

from backend.logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

def tell_me_about(topic) -> Optional[Any]:
    try:
        return wikipedia.summary(topic, sentences=3)
    except Exception as e:
        logger.error(e)
        return
