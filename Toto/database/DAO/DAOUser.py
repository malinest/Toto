"""
DAO for the users collection
"""

import Toto.database.db
from Toto.models.user import User
import Toto.utils.globals as g
from flask import jsonify

def getAllUsers():
    users = []
    collection = db.mongo[g.DATABASE_NAME]["Users"]
    result = collection.find({})
    for user in result:
        users.append(User.from_json(user))
    return users

def getUserByUsername(username):
    collection = db.mongo[g.DATABASE_NAME]["Users"]
    result = collection.find_one({"username": username})
    return User.from_json(result)