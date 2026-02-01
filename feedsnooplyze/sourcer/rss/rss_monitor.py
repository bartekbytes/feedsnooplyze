import requests
import hashlib
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List

# feedsnooplyze modules
from feedsnooplyze.sourcer.rss import Page, PageContent
from feedsnooplyze.parser import ParserBase
from feedsnooplyze.utils.content_comparer import ContentComparer
from feedsnooplyze.configuration.config import NotificationConfigBase
from feedsnooplyze.notifier import *


@dataclass
class PageMonitor:
    """
    Monitors a Web Page for content changes and runs configured Notifications when updates are detected.
    Attributes:
        page (Page): The Page to monitor.
        parser (ParserBase): The parser used to extract content from the page.
        last_hash (Optional[str]): The hash of the last known content.
        notifiers (Optional[List[NotificationConfigBase]]): List of Notification configurations.
    Methods:
        _get_content():
            Fetches the content from the page URL and parses it using the configured parser.
            Returns the parsed text content or None if parsing fails.
        _get_content_hash(content):
            Computes and returns the SHA-256 hash of the given content string.
        _make_notifiers_from_config(notification_config):
            Instantiates Notifier objects based on the provided Notification Configuration list.
        check_for_content_update(latest_persisted_hash, latest_persisted_content):
            Checks the page for content updates by comparing the current content hash with the latest persisted hash.
            If content has changed, notifies all configured Notifiers and returns a PageContent object with the update details.
            If no change is detected, returns a PageContent object indicating no update.
            On first run, saves the initial content and notifies all configured notifiers.
    """
    page: Page = field(default_factory=Page)
    parser: ParserBase = field(default_factory=ParserBase)
    last_hash: Optional[str] = None
    notifiers: Optional[List[NotificationConfigBase]] = None


    def _get_content(self):
        
        try:
        
            print(f"🚀 Request to a given URL [{self.page.url}] has been sent")
            response = requests.get(self.page.url, timeout=60)
            response.raise_for_status()
            
            # Parse obtained text from the URL based on the configured Parser
            print(f"📜 Parsing using [{self.parser.__class__.__name__}] parser") 
            content = self.parser.parse(response.text)
            
            if content:
                print(f"✅ Content has been found and parsed successfully")
                return content.get_text(separator = ' ', strip = True)
            else:
                print("❌ No Content or Content could not be parsed")
                return None
            
        except requests.exceptions.HTTPError as e: # HTTPError is raised for 4xx and 5xx responses
            print(f"❌ Error fetching {self.page.url}: {e}")
            print(f"HTTPError. Error: {e}")
        except requests.exceptions.RequestException as e: # All other request-related errors, includes connection errors, timeout errors, etc.
            print(f"❌ Error fetching {self.page.url}: {e}")
            print(f"RequestException. Error: {e}")
        except Exception as e: # Other exceptions that might occur
            print(f"❌ Error fetching {self.page.url}: {e}")
            print("Other error occurred:", e)





    def _get_content_hash(self, content):
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    

    def _make_notifiers_from_config(self, notification_config: List[NotificationConfigBase]) -> List[Notifier]:

        now_date = datetime.now()
        now = now_date.strftime("%Y-%m-%d %H:%M:%S")
        notifications = []
        for ncb in notification_config:
            notifier_name = ncb.__class__.__name__
            if notifier_name == "ConsoleNotificationConfig":
                notifications.append(ConsoleNotifier(page_name=self.page.name, content_time=now))
            elif notifier_name == "FlatFileNotificationConfig":
                notifications.append(FlatFileNotifier(file_path=ncb.file_path, page_name=self.page.name, content_time=now))
            elif notifier_name == "EmailNotificationConfig":
                notifications.append(EmailNotifier(email_address=ncb.email_address, email_password=ncb.email_password, recipients=ncb.recipients,
                                                   page_name=self.page.name, content_time=now, page_url=self.page.url))
            elif notifier_name == "TelegramNotificationConfig":
                notifications.append(TelegramNotifier(token=ncb.token, chat_id=ncb.chat_id, page_name=self.page.name, content_time=now, page_url=self.page.url))
                
        return notifications



    def check_for_content_update(self, latest_persisted_hash: str, latest_persisted_content: str) -> PageContent:
        
        print(f"\n🔍 Checking content for Page [{self.page.name}] ({self.page.url})")

        content = self._get_content()
        
        if content is None:
            return PageContent(page_name=None, content_time=None,  content_hash=None, full_content=None, added_content=None)
        
        current_hash = self._get_content_hash(content)
        
        # Case when we have persisted data
        if latest_persisted_hash:

            if current_hash != latest_persisted_hash:
                
                now = datetime.now()

                print(f"✅ Content has changed, current hash [{current_hash}], last hash [{latest_persisted_hash}]")
                self.last_hash = current_hash

                # Instantiate ContentComparer, compare a new and old content and get only added content
                cp = ContentComparer(new_string=content, old_string=latest_persisted_content)
                new_content = cp.get_difference()

                # Create Notifiers for NotificationConfig
                notifiers_list = self._make_notifiers_from_config(self.notifiers)
            
                # Create a main Notifier, register all Notifiers obtained from Config and run notify for all of them
                notifier = Notifier()
                [notifier.subscribe(n.notify) for n in notifiers_list]
                notifier.notify(new_content)
                
                return PageContent(page_name=self.page.name, content_time=now,
                                   content_hash=self.last_hash, full_content=latest_persisted_content, added_content=new_content)
        
            elif current_hash == latest_persisted_hash:
                
                print("⚠️ No changes detected.")

                now = datetime.now()
                return PageContent(page_name=None, content_time=now, content_hash=latest_persisted_hash, full_content=latest_persisted_content, added_content=None)

        elif not latest_persisted_hash and self.last_hash is None:
                
            self.last_hash = current_hash

            print(f"✅ Initial content saved, hash: [{self.last_hash}]")

            # Create Notifiers for NotificationConfig
            notifiers_list = self._make_notifiers_from_config(self.notifiers)
            
            # Create a main Notifier, register all Notifiers obtained from Config and run notify for all of them
            notifier = Notifier()
            [notifier.subscribe(n.notify) for n in notifiers_list]
            notifier.notify("Fist content for the Page")
            
            now = datetime.now()
            return PageContent(page_name=self.page.name, content_time=now,
                                content_hash=self.last_hash, full_content=content, added_content=content)
