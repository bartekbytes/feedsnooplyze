from dataclasses import dataclass

@dataclass
class RSSContent:
    """
    Represents the content details of a RSS feed.

    Attributes:
        title (str): The title of the RSS content.
        link_to_content (str): The URL link to the RSS content.
        content_summary (str): A summary of the RSS content.
        page_name (str): The name of the page or RSS feed.
        content_time (str): The timestamp when the content was captured or modified.
        content_hash (str): The hash value representing the content's integrity.
        full_content (str): The complete content of the page.
        added_content (str): The content that was added or changed since the last capture.
    """
    # Attributes for RSS Content
    title: str
    link_to_content: str
    content_summary: str
    
    # Attributes for Persistence Layer
    page_name: str
    content_time: str
    content_hash: str
    full_content: str
    added_content: str

