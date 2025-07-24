from .base_parser import ParserBase
from .parser_registry import PARSER_REGISTRY
from .generic_parsers import AllDocumentParser, MainElementParser, DivClassParser
from .custom_parsers import DuckDbBlogParser, MicrosoftAzureVirtualMachinesBlogParser, MicrosoftAzureAzureSQLDatabaseBlogParser

# Now, from persistence import PARSER_REGISTRY will work
__all__ = ["ParserBase", "PARSER_REGISTRY",
           
           "AllDocumentParser", "MainElementParser", "DivClassParser",
           
           "DuckDbBlogParser",
           "MicrosoftAzureVirtualMachinesBlogParser",
           "MicrosoftAzureAzureSQLDatabaseBlogParser"]