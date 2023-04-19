from dataclasses import dataclass
from datetime import datetime

@dataclass
class Post():
    """
    Class for the posts
    """
    id: int
    title: str
    username: str
    date: datetime
    media: str
    filename: str
    content: str
    comments: list[Comment]

    @staticmethod
    def from_json(json_dict):
        return Post(json_dict["id"], json_dict["title"], json_dict["username"], json_dict["date"], json_dict["media"], json_dict["filename"], json_dict["content"], json_dict["comments"])