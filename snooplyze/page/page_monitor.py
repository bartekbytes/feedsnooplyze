import requests
import hashlib
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

from .page import Page
from .page_content import PageContent
from parser import ParserBase


@dataclass
class PageMonitor:
    page: Page = field(default_factory=Page)
    parser: ParserBase = field(default_factory=ParserBase)
    #persistence: PersistenceEngine = field(default_factory=PersistenceEngine)
    timeout: int = 60
    last_hash: Optional[str] = None
    last_content: Optional[str] = None

    def _get_content(self):
        
        try:
        
            print(f"🚀 Request has been sent")
            response = requests.get(self.page.url, timeout = self.timeout)
            response.raise_for_status()
            
            content = self.parser.parse(response.text)
            
            if content:
                print(f"✅ Content has been found")
                return content.get_text(separator = ' ', strip = True)
            else:
                print("No CONTENT!!!! :(")
                return None
            
            print(content)
        
        except Exception as e:
            print(f"❌ Error fetching {self.page.url}: {e}")
            return None


    def _get_content_hash(self, content):
        return hashlib.sha256(content.encode('utf-8')).hexdigest()


    def check_for_update(self, latest_persisted_hash: str) -> PageContent:
        
        print(f"🔍 Checking content for {self.page.name} ({self.page.url})")

        content = self._get_content()
        
        if content is None:
            return PageContent(name=None, is_new=None, is_update=None, creation_time=None, update_time=None, hash=None, content=None)
        
        current_hash = self._get_content_hash(content)
        
        # Case when we have persisted data
        if latest_persisted_hash:

            if current_hash != latest_persisted_hash:
                
                print(f"✅ Content has changed, current hash: {self.current_hash}, last hash: {latest_persisted_hash}")
                self.last_hash = current_hash
            
                now = datetime.now()
                return PageContent(name=self.page.name, is_new=False, is_update=True, update_time=now, hash=self.last_hash, content=self.last_content)

                # TODO: Here will be a super important part - informing about the new content.
                # Sending info that the new content is available
                # Various channels can be involved: text on console, SMS, Telegram, Whatapp, Wechat, etc... 
        
            elif current_hash == latest_persisted_hash:
                
                print("⚠️ No change detected.")

                now = datetime.now()
                return PageContent(name=self.page.name, is_new=False, is_update=False, creation_time=None, update_time=None, hash=latest_persisted_hash, content=self.last_content)

        elif not latest_persisted_hash and self.last_hash is None:

            self.last_hash = current_hash

            print(f"✅ Initial content saved, hash: {self.last_hash}")
            
            now = datetime.now()
            return PageContent(name=self.page.name, is_new=True, is_update=False, creation_time=now, update_time=None, hash=self.last_hash, content=content)
        
        #if current_hash != self.last_hash:
            #print(f"✅ Content has changed, current hash: {self.current_hash}, last hash: {self.last_hash}")
            #self.last_hash = current_hash

            
            #now = datetime.now()
            #self.persistence.add_content(self.page.name, now, self.last_hash, content)
            #return PageContent(name=self.page.name, is_new=False, is_update=True, update_time=now, hash=self.last_hash, content=self.last_content)

            # TODO: Here will be a super important part - informing about the new content.
            # Sending info that the new content is available
            # Various channels can be involved: text on console, SMS, Telegram, Whatapp, Wechat, etc... 
        
        
        #else:
            #print("⚠️ No change detected.")

            #now = datetime.now()
            #self.persistence.add_content(self.page.name, now, self.last_hash, None)
            #return PageContent(name=self.page.name, is_new=False, is_update=False, creation_time=None, update_time=None, hash=self.last_hash, content=self.last_content)
