from dataclasses import dataclass
from typing import Optional

@dataclass
class Page:
    """
    Represents a Web Page with a name, URL, and optional description.

    Attributes:
        name (str): The name of the page.
        url (str): The URL of the page.
        description (Optional[str]): An optional description of the page.
    """
    name : str
    url : str
    description: Optional[str]