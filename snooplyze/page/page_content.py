from dataclasses import dataclass, field

@dataclass
class PageContent:
    name : str
    is_new : bool
    is_update : bool
    creation_time : str # TODO: make it datetime
    update_time : str # TODO: make it datetime
    hash : str
    content : str