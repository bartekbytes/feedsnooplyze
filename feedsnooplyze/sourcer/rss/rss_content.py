from dataclasses import dataclass

@dataclass
class RssContent:
    """
    Represents the content details of a RSS feed.

    Attributes:
        rss_name (str): The name of the Page.
        content_time (str): The timestamp when the content was captured or modified.
        content_hash (str): The hash value representing the content's integrity.
        full_content (str): The complete content of the page.
        added_content (str): The content that was added or changed since the last capture.
    """
    page_name: str
    content_time: str
    content_hash: str
    full_content: str
    added_content: str

