from .parser_base import ParserBase

PARSER_REGISTRY = {}


def register_parser_persistence(cls: type[ParserBase]):
    
    if not hasattr(cls, '__name__'):
        raise TypeError(f"Expected a class, got {type(cls).__name__}")
    
    key = cls.__name__.replace("Parser", "").lower()
    PARSER_REGISTRY[key] = cls
    return cls