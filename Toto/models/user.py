from dataclasses import dataclass
from datetime import datetime
import hashlibc
from io import BytesIO

@dataclass
class User():
    username: str
    email: str
    password: str
    profile_picture: BytesIO
    birthday: datetime
    creation_date: datetime

    @staticmethod
    def from_json(json_dict, **kwargs):
        return User(json_dict["username"], json_dict["email"], json_dict["password"], json_dict["profile_picture"], json_dict["birthday"], json_dict["creation_date"])