from abc import ABC, abstractmethod
from enum import Enum

class ParserType(str, Enum):
    ALL_DOCUMENT = "alldocument"
    MAIN_ELEMENT = "mainelement"
    DIV_CLASS = "divclass"


class ParserBase(ABC):
    
    @abstractmethod
    def parse(self, text_to_parse):
        pass