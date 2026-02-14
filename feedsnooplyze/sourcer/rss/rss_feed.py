from dataclasses import dataclass

@dataclass
class RSSFeed:
    """
    Represents the content details of a RSS Feed.

    Attributes:
        title (str): Title of the RSS Feed.
        link (str): URL to the content of the RSS Feed.
        published (str): When a given RSS Feed was published.
        summary (str): A summary of the content of the RSS Feed.
    """
    title: str
    link: str
    published: str
    summary: str

    def __str__(self):
        return(
            f"Title: {self.title}\n" +
            f"Link: {self.link}\n" #+ 
            f"Published: {self.published}\n" +
            f"Summary: {self.summary}\n"
        )
