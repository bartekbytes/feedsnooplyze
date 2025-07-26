import requests
import hashlib
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

# snooplyze modules
from page import Page, PageContent
from parser import ParserBase
from utils import ContentComparer


@dataclass
class PageMonitor:
    page: Page = field(default_factory=Page)
    parser: ParserBase = field(default_factory=ParserBase)
    last_hash: Optional[str] = None


    def _get_content(self):
        
        try:
        
            print(f"🚀 Request to a given URL {self.page.url} has been sent")
            response = requests.get(self.page.url, timeout=60)
            response.raise_for_status()
            
            # Parse obtained text from the URL based on the configured Parser 
            content = self.parser.parse(response.text)
            
            if content:
                print(f"✅ Content has been found and parsed successfully")
                return content.get_text(separator = ' ', strip = True)
            else:
                print("❌ No Content or Content could not be parsed")
                return None
            
        except Exception as e:
            print(f"❌ Error fetching {self.page.url}: {e}")
            return None


    def _get_content_hash(self, content):
        return hashlib.sha256(content.encode('utf-8')).hexdigest()


    def check_for_content_update(self, latest_persisted_hash: str, latest_persisted_content: str) -> PageContent:
        
        print(f"\n🔍 Checking content for Page [{self.page.name}] ({self.page.url})")

        content = self._get_content()
        
        if content is None:
            return PageContent(page_name=None, content_time=None,  content_hash=None, full_content=None, added_content=None)
        
        current_hash = self._get_content_hash(content)
        
        # Case when we have persisted data
        if latest_persisted_hash:

            if current_hash != latest_persisted_hash:
                
                print(f"✅ Content has changed, current hash: {current_hash}, last hash: {latest_persisted_hash}")
                self.last_hash = current_hash

                cp = ContentComparer(new_string=content, old_string=latest_persisted_content)
                new_content = cp.get_difference(name=self.last_hash)


                print("NOTIFIER HERE!")
                from notifier import Notifier, ConsoleNotifier, FileNotifier
                
                console_notifier = ConsoleNotifier()
                file_notifier = FileNotifier()
            
                notifier = Notifier()
                notifier.subscribe(console_notifier.notify)
                notifier.subscribe(file_notifier.notify)

                notifier.notify(current_hash)

                now = datetime.now()
                return PageContent(page_name=self.page.name, content_time=now,
                                   content_hash=self.last_hash, full_content=latest_persisted_content, added_content=new_content)
        
            elif current_hash == latest_persisted_hash:
                
                print("⚠️ No change detected.")

                now = datetime.now()
                return PageContent(page_name=None, content_time=now, content_hash=latest_persisted_hash, full_content=latest_persisted_content, added_content=None)

        elif not latest_persisted_hash and self.last_hash is None:

            self.last_hash = current_hash

            print(f"✅ Initial content saved, hash: {self.last_hash}")
            
            now = datetime.now()
            return PageContent(page_name=self.page.name, content_time=now,
                                content_hash=self.last_hash, full_content=content, added_content=content)
