from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List
import hashlib

# external modules
import feedparser
from feedparser import FeedParserDict

# feedsnooplyze modules
from feedsnooplyze.sourcer.rss import RSS, RSSContent #, TODO: RSSFeed circular import :/ fix later
from feedsnooplyze.utils.content_comparer import ContentComparer
from feedsnooplyze.configuration.config import NotificationConfigBase
from feedsnooplyze.notifier import *


@dataclass
class RSSMonitor:
    """
    Monitors a RSS for content changes and runs configured Notifications when updates are detected.
    Attributes:
        rss (RSS): The RSS to monitor.
        last_hash (Optional[str]): The hash of the last known content.
        notifiers (Optional[List[NotificationConfigBase]]): List of Notification configurations.
    Methods:
        _get_content():
            Fetches the content from the RSS URL.
            Returns the FeedParserDict content 
                (it's an internal feedparser objects that consists of the parsed RSS and RSS Feeds) 
            or None if parsing fails.
        _get_content_hash(content):
            Computes and returns the SHA-256 hash of the given content.
            As the content is in FeedParserDict object, str(content) is used to get a string representative.
        get_rss_feeds_raw():
            Returns a FeedParserDict, used for further extraction of RSSFeeds.
        _make_notifiers_from_config(notification_config):
            Instantiates Notifier objects based on the provided Notification Configuration list.
        check_for_content_update(latest_persisted_hash, latest_persisted_content):
            Checks the RSS for content updates by comparing the current content hash with the latest persisted hash.
            If content has changed, notifies all configured Notifiers and returns a RSSContent object with the update details.
            If no change is detected, returns a RSSContent object indicating no update.
            On first run, saves the initial content and notifies all configured notifiers.
    """
    rss: RSS = field(default_factory=RSS)
    last_hash: Optional[str] = None
    notifiers: Optional[List[NotificationConfigBase]] = None

    def _get_content(self) -> FeedParserDict | None:
        
        try:
            
            print(f"🚀 Request to a given RSS [{self.rss.url}] has been sent")
            feed = feedparser.parse(self.rss.url)

            if feed.bozo:
                print(f"❌ Error parsing RSS feed from {self.rss.url}: {feed.bozo_exception}")
                return None
            elif not feed:
                print(f"❌ No feed data found at {self.rss.url}")
                return None
            else:
                print(f"✅ RSS feed from {self.rss.url} has been parsed successfully")
                return feed
        except feedparser.bozo_exception as e:
            print(f"❌ Error parsing RSS feed from {self.rss.url}: {e}")
            return None 


    def _get_content_hash(self, content):
        # content is of type FeedParserDict, so we need to make it as string,
        # that's why we have str(content)
        return hashlib.sha256(str(content).encode('utf-8')).hexdigest()
    

    def get_rss_feeds_raw(self) -> FeedParserDict | None:
        return self._get_content()
    
    # TODO: Fix circular import
    #def get_rss_feeds(self) -> list[RSSFeed] | None:
    #    rss_feeds = []
    #    for feed in self._get_content().entries:
    #        rss_feeds.append(RSSFeed(feed.title, feed.link, feed.published, feed.summary))
    #    return rss_feeds


    def _make_notifiers_from_config(self, notification_config: List[NotificationConfigBase]) -> List[Notifier]:

        now_date = datetime.now()
        now = now_date.strftime("%Y-%m-%d %H:%M:%S")
        notifications = []
        for ncb in notification_config:
            notifier_name = ncb.__class__.__name__
            if notifier_name == "ConsoleNotificationConfig":
                notifications.append(ConsoleNotifier(page_name=self.rss.name, content_time=now))
            elif notifier_name == "FlatFileNotificationConfig":
                notifications.append(FlatFileNotifier(file_path=ncb.file_path, page_name=self.rss.name, content_time=now))
            elif notifier_name == "EmailNotificationConfig":
                notifications.append(EmailNotifier(email_address=ncb.email_address, email_password=ncb.email_password, recipients=ncb.recipients,
                                                   page_name=self.rss.name, content_time=now, page_url=self.rss.url))
            elif notifier_name == "TelegramNotificationConfig":
                notifications.append(TelegramNotifier(token=ncb.token, chat_id=ncb.chat_id, page_name=self.rss.name, content_time=now, page_url=self.rss.url))
                
        return notifications


    def check_for_content_update(self, latest_persisted_hash: str, latest_persisted_content: str) -> RSSContent:
        
        print(f"\n🔍 Checking content for RSS [{self.rss.name}] ({self.rss.url})")

        content = self._get_content()
        
        if content is None:
            return RSSContent(page_name=None, content_time=None,  content_hash=None, full_content=None, added_content=None)
        
        current_hash = self._get_content_hash(str(content))
        
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
                
                return RSSContent(rss_name=self.rss.name, content_time=now,
                                   content_hash=self.last_hash, full_content=latest_persisted_content, added_content=new_content
                                   )
        
            elif current_hash == latest_persisted_hash:
                
                print("⚠️ No changes detected.")

                now = datetime.now()
                return RSSContent(page_name=None, content_time=now,
                                  content_hash=latest_persisted_hash, full_content=latest_persisted_content, added_content=None
                                  )

        elif not latest_persisted_hash and self.last_hash is None:
                
            self.last_hash = current_hash

            print(f"✅ Initial content saved, hash: [{self.last_hash}]")

            # Create Notifiers for NotificationConfig
            notifiers_list = self._make_notifiers_from_config(self.notifiers)
            
            # Create a main Notifier, register all Notifiers obtained from Config and run notify for all of them
            notifier = Notifier()
            [notifier.subscribe(n.notify) for n in notifiers_list]
            notifier.notify("Fist content for the RSS")
            
            now = datetime.now()
            return RSSContent(rss_name=self.rss.name, content_time=now,
                              content_hash=self.last_hash, full_content=content, added_content=content
                              )