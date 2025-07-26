from dataclasses import dataclass

@dataclass
class PageContent:
    page_name: str
    content_time: str
    content_hash: str
    full_content: str
    added_content: str

