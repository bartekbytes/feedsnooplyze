class Notifier:
    def __init__(self):
        self.subscribers = []

    def subscribe(self, callback):
        self.subscribers.append(callback)

    def notify(self, message):
        for callback in self.subscribers:
            callback(message)