from feedsnooplyze.notifier import Notifier

class ConsoleNotifier(Notifier):
    """
    ConsoleNotifier is a notifier implementation that outputs notifications to the console.
    Attributes:
        page_name (str): The name of the page associated with the notification.
        content_time (str): The timestamp or time associated with the content.
    Methods:
        __init__(page_name, content_time):
            Initializes the ConsoleNotifier with the page name and content time.
        notify(message):
            Prints a formatted notification message to the console, including the time, page name, and content.
            Args:
                message (str): The message content to be displayed in the notification.
    """

    def __init__(self, page_name: str, content_time: str):
        self.page_name = page_name
        self.content_time = content_time
    
    def notify(self, message):
        print(f"\n| 🔔\n| Time: {self.content_time} | Page: {self.page_name}\n| Content:\n| {message}/n")