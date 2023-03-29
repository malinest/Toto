"""

File that handles the database connection

"""

from pymongo import MongoClient

class Mongo():

    connection = None

    def create_connection(self):
        connection = MongoClient("")