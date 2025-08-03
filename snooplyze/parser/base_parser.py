from abc import ABC, abstractmethod
from enum import Enum, auto

class ParserType(str, Enum):
    """
    Enum representing different types of parsers for document processing.
    Attributes:
        ALL_DOCUMENT: Parser for the entire document.
        MAIN_ELEMENT: Parser for the main element of the document.
        DIV_CLASS: Parser for specific div classes within the document.
        DUCKDB_BLOG: Parser specialized for DuckDB blog documents.
        MICROSOFT_AZURE_VIRTUAL_MACHINES_BLOG: Parser for Microsoft Azure Virtual Machines blog documents.
        MICROSOFT_AZURE_AZURE_SQL_DATABASE_BLOG: Parser for Microsoft Azure SQL Database blog documents.
    """
    
    # Generic Parsers
    ALL_DOCUMENT = "all_document"
    MAIN_ELEMENT = "main_element"
    DIV_CLASS = "div_class"

    # Custom Parsers
    DUCKDB_BLOG = "duckdb_blog"
    MICROSOFT_AZURE_VIRTUAL_MACHINES_BLOG = "microsoft_azure_virtual_machines_blog"
    MICROSOFT_AZURE_AZURE_SQL_DATABASE_BLOG = "microsoft_azure_azure_sql_database_blog"

class ParserBase(ABC):
    """
    Abstract base class for parsers.
    This class defines the interface for parser implementations. Subclasses must implement
    the `parse` method, which takes a string input and processes it according to the parser's logic.
    Methods
    -------
    parse(text_to_parse: str)
        Abstract method to parse the given text. Must be implemented by subclasses.
    """
    
    @abstractmethod
    def parse(self, text_to_parse):
        pass