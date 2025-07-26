from bs4 import BeautifulSoup
from typing import Any
from dataclasses import dataclass

from .base_parser import ParserBase



class AllDocumentParser(ParserBase):
    """
    Extracts the whole HTML document
    """
    
    def __init__(self):
        pass

    def parse(self, text_to_parse) -> Any | None:
            
            soup = BeautifulSoup(text_to_parse, 'html.parser')
            content = soup.body
            
            if content:
                return content
            else:
                return None
            

class MainElementParser(ParserBase):
    """
    Extracts only the part of HTML document that it's within <main></main> part
    """    
    
    def __init__(self):
        pass

    def parse(self, text_to_parse) -> Any | None:
        
        soup = BeautifulSoup(text_to_parse, 'html.parser')
        content = soup.find('main')

        if content:
            return content
        else:
            return None
    

@dataclass
class DivClassParser(ParserBase):
    """
    Extracts the <div></div> part of the HTML document that has a given div_class_name class
    """
    class_name: str

    def parse(self, text_to_parse) -> Any | None:

        soup = BeautifulSoup(text_to_parse, 'html.parser')
        content = soup.find('div', class_ = self.class_name)
    
        if content:
            return content
        else:
            return None
