import requests
from snooplyze.notifier import Notifier


class TelegramNotifier(Notifier):
    """
    TelegramNotifier is a notifier class for sending messages via Telegram Bot API.
    Attributes:
        token (str): Telegram bot token used for authentication.
        chat_id (str): Telegram chat ID where notifications will be sent.
        page_name (str): Name of the page associated with the notification.
        content_time (str): Timestamp or time information related to the content.
        page_url (str): URL of the page associated with the notification.
    Methods:
        __init__(token, chat_id, page_name, content_time, page_url):
            Initializes the TelegramNotifier with the bot token, chat ID, page name, content time, and page URL.
        notify(message):
            Sends a notification message to the specified Telegram chat.
            The message includes the page name, content time, page URL, and the provided message.
            Handles HTTP and request exceptions, printing error details if sending fails.
    """

    def __init__(self, token: str, chat_id: str, page_name: str, content_time: str, page_url: str):
        self.token = token
        self.chat_id = chat_id  
        self.page_name = page_name
        self.content_time = content_time    
        self.page_url = page_url


    def notify(self, message):

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": f"Snooplyze - New Content\n{self.page_name} - {self.content_time}\n{self.page_url}\n\n{message}"
        }

        try:
            response = requests.post(url, data=payload)
            response.raise_for_status()  # Raise an error for bad responses
            
            print(f"🔔 Telegram Notification for [{self.page_name}] sent successfully.")
        
        except requests.exceptions.HTTPError as e: # HTTPError is raised for 4xx and 5xx responses
            print(f"❌ Telegram Notification for [{self.page_name}] failed to send.")
            print(f"HTTPError. Error: {e}")
        except requests.exceptions.RequestException as e: # All other request-related errors, includes connection errors, timeout errors, etc.
            print(f"❌ Telegram Notification for [{self.page_name}] failed to send.")
            print(f"RequestException. Error: {e}")
        except Exception as e: # Other exceptions that might occur
            print(f"❌ Telegram Notification for [{self.page_name}] failed to send.")
            print("Other error occurred:", e)
        


        

