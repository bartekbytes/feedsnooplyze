from typing import Any
from bs4 import BeautifulSoup

from .base_parser import ParserBase


class DuckDbBlogParser(ParserBase):
    """
    DuckDbBlogParser is a custom parser for extracting content from DuckDB blog pages.
    Methods
    -------
    __init__():
        Initializes the DuckDbBlogParser instance.
    parse(text_to_parse: str) -> Any | None:
        Parses the provided HTML text and extracts the content within the <div> element
        with class "newstiles". Returns the extracted content if found, otherwise returns None.
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