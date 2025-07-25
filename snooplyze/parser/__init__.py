from .base_parser import ParserBase, ParserType
from .generic_parsers import AllDocumentParser, MainElementParser, DivClassParser
from .custom_parsers import DuckDbBlogParser, MicrosoftAzureVirtualMachinesBlogParser, MicrosoftAzureAzureSQLDatabaseBlogParser

# Now, from persistence import PARSER_REGISTRY will work
__all__ = ["ParserBase", "ParserType",
           
           "AllDocumentParser", "MainElementParser", "DivClassParser",
           
           "DuckDbBlogParser",
           "MicrosoftAzureVirtualMachinesBlogParser",
           "MicrosoftAzureAzureSQLDatabaseBlogParser"]