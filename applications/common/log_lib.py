import uuid
import logging
import datetime
from logging.config import dictConfig

from applications.core import settings


class Logger:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.log()

    @staticmethod
    def log():
        dictConfig(settings.LOGGING)