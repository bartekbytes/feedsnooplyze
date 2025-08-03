from .base_parser import ParserBase, ParserType
from .parser_registry import get_parser
from .generic_parsers import AllDocumentParser, MainElementParser, DivClassParser
from .custom_parsers import DuckDbBlogParser

# Now, from persistence import PARSER_REGISTRY will work
__all__ = ["ParserBase", "ParserType",
           "get_parser",
           
           "AllDocumentParser", "MainElementParser", "DivClassParser",
           
           "DuckDbBlogParser"]