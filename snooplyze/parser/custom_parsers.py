from typing import Any
from bs4 import BeautifulSoup

from .base_parser import ParserBase


class DuckDbBlogParser(ParserBase):
    """
    Extracts the content of Duck DB blog
    """

    def __init__(self):
        pass

    def parse(self, text_to_parse) -> Any | None:

        soup = BeautifulSoup(text_to_parse, 'html.parser')
        content = soup.find('div', class_ = "newstiles")
    
        if content:
            return content
        else:
            return None
        
class MicrosoftAzureVirtualMachinesBlogParser(ParserBase):

    def __init__(self):
        pass

    def parse(self, text_to_parse) -> Any | None:
        
        soup = BeautifulSoup(text_to_parse, 'html.parser')
        content = soup.find('div', class_ = "search-results__posts faceted-search__posts")

        if content:
            return content
        else:
            return None

class MicrosoftAzureAzureSQLDatabaseBlogParser(ParserBase):
    
    def __init__(self):
        pass

    def parse(self, text_to_parse) -> Any | None:
        
        soup = BeautifulSoup(text_to_parse, 'html.parser')
        content = soup.find('div', class_ = "search-results__posts faceted-search__posts")
        
        if content:
            return content
        else:
            return None