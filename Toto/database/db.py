"""
File that handles the database connection
"""

import sys

from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

import Toto.utils.globals as g
from Toto.utils.logs import logger

mongo = MongoClient(g.DATABASE_URL)
try:
    mongo.admin.command('ping')
    logger.debug("Connection to the database created successfully")
except ConnectionFailure:
    logger.critical("Couldn't establish a connection to the database")
    sys.exit()