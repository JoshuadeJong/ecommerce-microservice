from dotenv import load_dotenv
from pathlib import Path
import os
import logging

# set path to env file
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


class ConfigFlask:
    HOST = os.getenv("FLASK_HOST")
    PORT = os.getenv("FLASK_PORT")
    SECRET = os.getenv("FLASK_SECRET")


class ConfigCatalog:
    HOST = os.getenv("CATALOG_HOST")
    PORT = os.getenv("CATALOG_PORT")


class ConfigCart:
    HOST = os.getenv("CART_HOST")
    PORT = os.getenv("CART_PORT")


class ConfigLog:
    _logging = os.getenv("LOGGING")
    if _logging == "info":
        LOGGING = logging.INFO
    elif _logging == "warning":
        LOGGING = logging.WARNING
    elif _logging == "error":
        LOGGING = logging.ERROR