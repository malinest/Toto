"""
Script that creates the required mongodb database.
The script takes 2 arguments:
    1. The connection string to mongodb with the following format: 'mongodb://username:password@ip:port'
    2. The desired database name, for example: 'TotoDB'
"""

import sys

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

if __name__ == "__main__":
    if len(sys.argv == 3):
        connection = MongoClient(sys.argv[1])
        try:
            mongo.admin.command('ping')
        except ConnectionFailure:
            print("Couldn't connect to the database")
        try:
            database = connection[sys.argv[3]]
            database.create_collection(name="Boards")
            database.create_collection(name="Counters")
            database.create_collection(name="Users")
            print("All boards created successfully")
        except OperationFailure:
            print("Couldn't create the boards")
    else:
        raise ValueError("This scripts only takes 2 arguments (uri/database_name) ({0} supplied)".format(len(args)))