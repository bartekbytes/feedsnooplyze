from enum import Enum
from typing import List


class NotifierType(str, Enum):
    CONSOLE = "CONSOLE"
    FLATFILE = "FLATFILE"
    EMAIL = "EMAIL"


class Notifier():
    def __init__(self):
        self.subscribers = []
    
    def subscribe(self, callback):
        self.subscribers.append(callback)

    def notify(self, message):
        for callback in self.subscribers:
            callback(message)