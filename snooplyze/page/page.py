from dataclasses import dataclass
from typing import Optional

@dataclass
class Page:
    name : str
    url : str
    description: Optional[str]