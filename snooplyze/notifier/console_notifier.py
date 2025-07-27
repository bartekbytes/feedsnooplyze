from notifier import Notifier

class ConsoleNotifier(Notifier):

    def __init__(self, page_name: str, content_time: str):
        self.page_name = page_name
        self.content_time = content_time
    
    def notify(self, message):
        print(f"🔔 {self.content_time} | {self.page_name} | {message}")