from abc import ABC, abstractmethod
from enum import Enum
from typing import List


class NotifierType(str, Enum):
    """
    Enum representing the types of notifiers available.

    Attributes:
        CONSOLE: Notifier that outputs messages to the console.
        FLATFILE: Notifier that writes messages to a flat file.
        EMAIL: Notifier that sends messages via email.
        TELEGRAM: Notifier that sends messages via Telegram.
    """
    CONSOLE = "CONSOLE"
    FLATFILE = "FLATFILE"
    EMAIL = "EMAIL"
    TELEGRAM = "TELEGRAM"


class Notifier():
    """
    Notifier is a base class for managing and notifying subscribers.
    Attributes:
        subscribers (list): A list of callback functions to be notified.
    Methods:
        __init__():
            Initializes the Notifier with an empty list of subscribers.
        subscribe(callback):
            Registers a callback function to be notified.
        notify(message):
            Abstract method. Notifies all registered subscribers with the provided message.
            Must be implemented by subclasses.
    """
    def __init__(self):
        self.subscribers = []
    
    def subscribe(self, callback):
        self.subscribers.append(callback)

    @abstractmethod
    def notify(self, message):
        for callback in self.subscribers:
            callback(message)