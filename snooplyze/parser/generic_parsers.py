from bs4 import BeautifulSoup
from typing import Any
from dataclasses import dataclass

from .base_parser import ParserBase



class AllDocumentParser(ParserBase):
    """
    AllDocumentParser is a parser class that extracts the <body> content from an HTML document.
    Methods
    -------
    __init__():
        Initializes the AllDocumentParser instance.
    parse(text_to_parse: str) -> Any | None:
        Parses the given HTML text and returns the content of the <body> tag if present.
        Returns None if the <body> tag is not found.
        Parameters:
            text_to_parse (str): The HTML text to be parsed.
        Returns:
            Any | None: The parsed <body> content or None if not found.
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
    MainElementParser extracts the <main> HTML element from a given HTML string.
    This parser uses BeautifulSoup to parse the input HTML and searches for the first <main> element.
    If found, it returns the BeautifulSoup Tag object representing the <main> element; otherwise, it returns None.
    Methods
    -------
    __init__():
        Initializes the MainElementParser instance.
    parse(text_to_parse: str) -> Any | None:
        Parses the provided HTML string and returns the <main> element if present, else None.
    Parameters
    ----------
    text_to_parse : str
        The HTML content to be parsed.
    Returns
    -------
    Any | None
        The <main> element as a BeautifulSoup Tag object if found, otherwise None.
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
    Parses HTML content to extract a <div> element with a specified class name.
    Attributes:
        class_name (str): The class name to search for within <div> elements.
    Methods:
        parse(text_to_parse: str) -> Any | None:
            Parses the provided HTML text and returns the first <div> element
            matching the specified class name. Returns None if no such element is found.
    """
    class_name: str

    def parse(self, text_to_parse) -> Any | None:

        soup = BeautifulSoup(text_to_parse, 'html.parser')
        content = soup.find('div', class_ = self.class_name)
    
        if content:
            return content
        else:
            return None
