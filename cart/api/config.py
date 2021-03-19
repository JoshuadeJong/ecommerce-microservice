from dotenv import load_dotenv
from pathlib import Path
import os
import logging

# set path to env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class ConfigFast:
    PORT = int(os.getenv("FAST_PORT"))


class ConfigRedis:
    HOST = os.getenv("REDIS_HOST")
    PORT = os.getenv("REDIS_PORT")
    URI = f"redis://{HOST}:{PORT}"


class ConfigLog:
    _logging = os.getenv("LOGGING")
    if _logging == "info":
        LOGGING = logging.INFO
    elif _logging == "warning":
        LOGGING = logging.WARNING
    elif _logging == "error":
        LOGGING = logging.ERROR