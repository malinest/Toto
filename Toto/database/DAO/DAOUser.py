"""
DAO for the users collection
"""

import Toto.database.db
from Toto.models.user import User
from flask import jsonify

def getAllUsers():
    users = []
    collection = db.mongo["TotoDB"]["Users"]
    result = collection.find({})
    for user in result:
        users.append(User.from_json(user))
    return users

def getUserByUsername(username):
    collection = db.mongo["TotoDB"]["Users"]
    result = collection.find_one({"username": username})
    return User.from_json(result)