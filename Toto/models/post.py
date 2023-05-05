from dataclasses import dataclass
from datetime import datetime
from io import BytesIO

from Toto.models.comment import Comment

@dataclass
class Post():
    """
    Class for the posts
    """
    id: int
    title: str
    username: str
    date: datetime
    filename: str
    content: str
    comments: list[Comment]

    def to_dict(self):
        return {"_id": self.id, "title": self.title, "username": self.username, "date": self.date, "filename": self.filename, "content": self.content, "comments": self.comments}

    @staticmethod
    def from_json(json_dict):
        return Post(json_dict["_id"], json_dict["title"], json_dict["username"], json_dict["date"], json_dict["filename"], json_dict["content"], json_dict["comments"])