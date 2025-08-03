from .base_parser import ParserBase, ParserType
from .generic_parsers import *
from .custom_parsers import *

PARSER_REGISTRY = {
    # Generic Parsers
    ParserType.ALL_DOCUMENT: AllDocumentParser,
    ParserType.MAIN_ELEMENT: MainElementParser,
    ParserType.DIV_CLASS: DivClassParser,
    
    # Custom Parsers
    ParserType.DUCKDB_BLOG: DuckDbBlogParser,
    ParserType.MICROSOFT_AZURE_VIRTUAL_MACHINES_BLOG: MicrosoftAzureVirtualMachinesBlogParser,
    ParserType.MICROSOFT_AZURE_AZURE_SQL_DATABASE_BLOG: MicrosoftAzureAzureSQLDatabaseBlogParser,
}

def get_parser(parser_type: ParserType) -> ParserBase:
    """
    Returns the parser class based on the parser type.
    """
    if parser_type in PARSER_REGISTRY:
        return PARSER_REGISTRY[parser_type]()
    else:
        raise ValueError(f"Parser type '{parser_type}' is not registered.")
    