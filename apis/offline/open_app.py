import os

import AppOpener

from logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

class OpenApp:
    def __init__(self, app_name):
        try:
            AppOpener.open(
                app_name, 
                match_closest=True, 
                output=False
            )
        except Exception as e:
            logger.error(f'Opening App Failed: {e}')