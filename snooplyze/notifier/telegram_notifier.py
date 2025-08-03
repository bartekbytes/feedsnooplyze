import requests
from notifier import Notifier


class TelegramNotifier(Notifier):

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
        


        

