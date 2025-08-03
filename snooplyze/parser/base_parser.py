from abc import ABC, abstractmethod
from enum import Enum, auto

class ParserType(str, Enum):
    ALL_DOCUMENT = "all_document"
    MAIN_ELEMENT = "main_element"
    DIV_CLASS = "div_class"

    DUCKDB_BLOG = "duckdb_blog"
    MICROSOFT_AZURE_VIRTUAL_MACHINES_BLOG = "microsoft_azure_virtual_machines_blog"
    MICROSOFT_AZURE_AZURE_SQL_DATABASE_BLOG = "microsoft_azure_azure_sql_database_blog"

class ParserBase(ABC):
    
    @abstractmethod
    def parse(self, text_to_parse):
        pass