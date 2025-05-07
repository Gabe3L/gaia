import os
import datetime
import subprocess

from backend.logs.logging_setup import setup_logger

################################################################

file_name = os.path.splitext(os.path.basename(__file__))[0]
logger = setup_logger(file_name)

################################################################

def write_note(text):
    try:
        date = datetime.datetime.now()
        file_name = str(date).replace(":", "-") + "-note.txt"
        with open(file_name, "w") as f:
            f.write(text)
        notepad = "C://Program Files (x86)//Notepad++//notepad++.exe"
        subprocess.Popen([notepad, file_name])
    except Exception as e:
        logger.error(e)