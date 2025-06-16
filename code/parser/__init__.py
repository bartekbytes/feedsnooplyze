from .parser_registry import PARSER_REGISTRY

# Explicitly import modules so decorators execute and register classes
from . import parser_base
from . import custom_parsers
from . import generic_parsers

# Now, from persistence import PARSER_REGISTRY will work
__all__ = ["PARSER_REGISTRY"]    