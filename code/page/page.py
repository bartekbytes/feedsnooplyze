import requests
from bs4 import BeautifulSoup
import hashlib
from datetime import datetime

from data_parse.data_parse import DataParse
from persistence.persistence_engine import PersistenceEngine


class Page:
    def __init__(self, name: str, url: str = None):
        self.name = name
        self.url = url



class PageMonitor:

    def __init__(self, page: Page, parser : DataParse, persistence : PersistenceEngine, timeout : int = 10):
        self.page = page or Page()
        self.parser = parser or DataParse()
        self.persistence = persistence or PersistenceEngine()
        self.timeout = timeout
        self.last_hash = None


    def process_content(self):
        
        try:
        
            print(f"🚀 Request has been sent")
            response = requests.get(self.page.url, timeout=self.timeout)
            response.raise_for_status()
            
            content = self.parser.parse(response.text)
            
            if content:
                print(f"✅ Content has been found")
                #print(content.get_text(separator = ' ', strip=True)) # to remove
                return content.get_text(separator = ' ', strip=True)
        
        except Exception as e:
            print(f"❌ Error fetching {self.page.url}: {e}")
            return None


    def _get_content_hash(self, content):
        return hashlib.sha256(content.encode('utf-8')).hexdigest()


    def check_for_update(self):
        
        print(f"🔍 Checking content for {self.page.name} ({self.page.url})")

        content = self.process_content()
        
        if content is None:
            return False
        
        current_hash = self._get_content_hash(content)
        
        if self.last_hash is None:
            self.last_hash = current_hash

            print(f"✅ Initial content saved, hash: {self.last_hash}")

            
            now = datetime.now()
            self.persistence.add_content(self.page.name, now, self.last_hash, content)

            return False
        
        if current_hash != self.last_hash:
            print(f"✅ Content has changed, current hash: {self.current_hash}, last hash: {self.last_hash}")
            self.last_hash = current_hash

            
            now = datetime.now()
            self.persistence.add_content(self.page.name, now, self.last_hash, content)


            return True
        else:
            print("⚠️ No change detected.")

            now = datetime.now()
            self.persistence.add_content(self.page.name, now, self.last_hash, None)
            return False
