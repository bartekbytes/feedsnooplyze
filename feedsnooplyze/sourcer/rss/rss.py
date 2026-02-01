from dataclasses import dataclass
from typing import Optional

@dataclass
class RSS:
    """
    Represents a RSS with a name, URL, and optional description.

    Attributes:
        name (str): The name of the RSS.
        url (str): The URL of the RSS.
        description (Optional[str]): An optional description of the RSS.
    """
    name : str
    url : str
    description: Optional[str]