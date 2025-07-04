from bs4 import BeautifulSoup
from typing import Any

from parser.parser_base import ParserBase
from .parser_registry import register_parser_persistence



@register_parser_persistence
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
            
    @classmethod
    def validate(cls, data: dict):
        pass
        #missing = [f for f in ("type") if f not in data]
        #if missing:
            #raise ValueError(f"[AllDocumentParser] - missing fields for parser: {', '.join(missing)}")

    
@register_parser_persistence
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
    

    @classmethod
    def validate(cls, data: dict):
        pass
        #missing = [f for f in ("type") if f not in data]
        #if missing:
            #raise ValueError(f"[MainElementParser] - missing fields for parser: {', '.join(missing)}")

from dataclasses import dataclass

@dataclass
@register_parser_persistence
class DivClassParser(ParserBase):
    """
    Extracts the <div></div> part of the HTML document that has a given div_class_name class
    """
    class_name: str
    #def __init__(self, class_name: str):
        #self.class_name = class_name


    def parse(self, text_to_parse) -> Any | None:
        print("INSIDE")
        print(self.class_name)
        #print(text_to_parse)

        soup = BeautifulSoup(text_to_parse, 'html.parser')
        content = soup.find('div', class_ = self.class_name)
    
        if content:
            return content
        else:
            return None


    @classmethod
    def validate(cls, data: dict):
        if "class_name" not in data:
            raise ValueError("[DivClassParser] - missing field 'class_name' for parser")