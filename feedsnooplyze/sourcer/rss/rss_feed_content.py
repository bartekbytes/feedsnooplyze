from dataclasses import dataclass

@dataclass
class RSSFeedContent:
    """
    Represents the content details of a RSS Feed including feedsnooplyzer technicla fields.

    Attributes:
        rss_name (str): The name of the RSS.
        rss_name (str): The name of the RSS Feed for a given RSS.
        content_time (str): The timestamp when the content was captured or modified.
        content_hash (str): The hash value representing the content's integrity.
        full_content (str): The complete content of the RSS Feed.
        added_content (str): The content that was added or changed since the last capture.
        title (str): Title of the RSS Feed.
        link (str): URL to the content of the RSS Feed.
        published (str): When a given RSS Feed was published.
        summary (str): A summary of the content of the RSS Feed.
    """
    rss_name: str
    rss_feed_name: str
    content_time: str
    content_hash: str
    full_content: str
    added_content: str
    title: str
    link: str
    published: str
    summary: str

