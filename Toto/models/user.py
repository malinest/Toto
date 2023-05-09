from dataclasses import dataclass
from datetime import datetime
from io import BytesIO

@dataclass
class User():
    """
    Class for the posts
    """
    username: str
    email: str
    password: str
    creation_date: datetime

    def to_dict(self):
        return {"username": self.username, "email": self.email, "password": self.password, "creation_date": self.creation_date}

    @staticmethod
    def from_json(json_dict, **kwargs):
        return User(json_dict["username"], json_dict["email"], json_dict["password"], json_dict["creation_date"])