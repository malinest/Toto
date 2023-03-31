"""
File that handles the database connection
"""

from pymongo import MongoClient
import Toto.utils.globals as g

mongo = MongoClient(g.DATABASE_URL)