"""
DAO for the users collection
"""

import Toto.database.db as db
from Toto.models.user import User
import Toto.utils.globals as g
from flask import jsonify

def getAllUsers() -> list[User]:
    """
    Retrieves all the users from the database
    """
    users = []
    collection = db.mongo[g.DATABASE_NAME]["Users"]
    result = collection.find({})
    for user in result:
        users.append(User.from_json(user))
    return users

def getUserByUsername(username) -> User:
    """
    Retrieves a single user by it's username, if the user isn't found it will return None
    Example:
        username: Juan
    """
    collection = db.mongo[g.DATABASE_NAME]["Users"]
    result = collection.find_one({"username": username})
    if result:
        return User.from_json(result)
    else:
        return None