import os
import psutil

import AppOpener

from backend.logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

class OpenApp:
    def __init__(self):
        pass

    @staticmethod
    def open_app(app_name):
        try:
            AppOpener.open(
                app_name, 
                match_closest=True, 
                output=False
            )
        except Exception as e:
            logger.error(f'Opening App Failed: {e}')
    
    @staticmethod
    def is_app_open(app_name):
        for proc in psutil.process_iter(['name']):
            try:
                if app_name in proc.info['name'].lower():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False