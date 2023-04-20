from dataclasses import dataclass
from datetime import datetime

@dataclass
class Comment():
    """
    Class for the comments
    """
    id: int
    username: str
    date: datetime
    media: str
    filename: str
    content: str