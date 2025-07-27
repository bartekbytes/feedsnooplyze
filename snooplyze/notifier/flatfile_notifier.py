from notifier import Notifier

class FlatFileNotifier(Notifier):

    def __init__(self, file_path: str, page_name: str, content_time: str):
        self.file_path = file_path
        self.page_name = page_name
        self.content_time = content_time

    def notify(self, message):
        with open(self.file_path, "a") as f:
            f.write(f"{self.content_time} | {self.page_name} | {message}" + "\n")