"""
DAO for the 'Boards' collection
"""

import json
import Toto.database.db as db
from Toto.models.board import Board
from Toto.utils.logs import logger

def getAllBoards():
    """
    Retrieves all the boards from the database and returns a list of them
    """
    boards = []
    collection = db.mongo["TotoDB"]["Boards"]
    result = collection.find({})
    for board in result:
        boards.append(Board.from_json(board))
    logger.debug("Retrieved {0} boards".format(len(boards)))
    return boards