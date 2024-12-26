import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%Y-%m-%d')}.log"
logs_dir = os.path.join(os.getcwd(), 'logs', LOG_FILE)
os.makedirs(logs_dir, os.path.exists(logs_dir))

LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

logging.basicConfig(filename=LOG_FILE_PATH, level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == "__main__":
    logging.debug("This is a debug message")
    logging.info("This is an info message")
    logging.warning("This is a warning message")
    logging.error("This is an error message")
    logging.critical("This is a critical message")
    