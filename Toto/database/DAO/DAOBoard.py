"""
DAO for the 'Boards' collection
"""

import Toto.database.db as db
from Toto.models.board import Board
from Toto.utils.logs import logger
import Toto.utils.globals as g

def getAllBoards():
    """
    Retrieves all the boards from the database and returns a list of them
    """
    boards = []
    collection = db.mongo[g.DATABASE_NAME]["Boards"]
    result = collection.find({})
    for board in result:
        boards.append(Board.from_json(board))
    logger.debug("Retrieved {0} boards".format(len(boards)))
    return boards

def getBoardByAbbreviation(boardAbbreviation):
    """
    Retrieves a board by it's abbreviation
    """
    collection = db.mongo[g.DATABASE_NAME]["Boards"]
    result = collection.find_one({'abbreviation': boardAbbreviation})
    return Board.from_json(result)

def checkIfBoardExists(board_collection_name):
    """
    Checks if a board exists and returns a boolean depending on the result
    Input example: "Board_Technology"
    """
    collection = db.mongo[g.DATABASE_NAME]["Boards"]
    result = collection.find_one({"collection_name": board_collection_name})
    return True if result else False