from .base_parser import ParserBase, ParserType
from .generic_parsers import *
from .custom_parsers import *


PARSER_REGISTRY = {
    # Generic Parsers
    ParserType.ALL_DOCUMENT: AllDocumentParser,
    ParserType.MAIN_ELEMENT: MainElementParser,
    ParserType.DIV_CLASS: DivClassParser,
    
    # Custom Parsers
    ParserType.DUCKDB_BLOG: DuckDbBlogParser
}

def get_parser(parser_type: ParserType) -> ParserBase:
    """
    Retrieves a parser instance based on the specified parser type.
    Args:
        parser_type (ParserType): The type of parser to retrieve.
    Returns:
        ParserBase: An instance of the requested parser.
    Raises:
        ValueError: If the specified parser type is not registered.
    """

    if parser_type in PARSER_REGISTRY:
        return PARSER_REGISTRY[parser_type]()
    else:
        raise ValueError(f"Parser type '{parser_type}' is not registered.")
    