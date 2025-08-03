from notifier import Notifier

class FlatFileNotifier(Notifier):
    """
    FlatFileNotifier is a notifier that appends messages to a flat file.
    Args:
        file_path (str): The path to the file where notifications will be written.
        page_name (str): The name of the page associated with the notification.
        content_time (str): The timestamp or time string associated with the content.
    Methods:
        __init__(file_path, page_name, content_time):
            Initializes the FlatFileNotifier with the file path, page name, and content time.
        notify(message):
            Appends a notification message to the specified file, including the content time and page name.
            Each message is written in the format: "<content_time> | <page_name> | <message>"
    """

    def __init__(self, file_path: str, page_name: str, content_time: str):
        self.file_path = file_path
        self.page_name = page_name
        self.content_time = content_time

    def notify(self, message):
        with open(self.file_path, "a") as f:
            f.write(f"{self.content_time} | {self.page_name} | {message}" + "\n")