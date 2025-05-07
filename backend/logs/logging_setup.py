import os
import logging

LOG_LEVEL: int = logging.DEBUG

def setup_logger(file_name):
    log_dir = "logs/files"
    os.makedirs(log_dir, exist_ok=True)
    
    log_file_path = os.path.join(log_dir, f"{file_name}.log")
    
    with open(log_file_path, 'w'):
        pass
    
    if not os.path.exists(log_file_path):
        open(log_file_path, 'a').close()

    logger = logging.getLogger(file_name)
    logger.setLevel(LOG_LEVEL)

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(LOG_LEVEL)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    if not logger.hasHandlers():
        logger.addHandler(file_handler)

    return logger