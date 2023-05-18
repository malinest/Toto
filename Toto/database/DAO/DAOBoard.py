"""
DAO for the 'Boards' collection
"""

import Toto.database.db as db
import Toto.utils.globals as g
from Toto.models.board import Board
from Toto.utils.logs import logger

def getAllBoards() -> list(Board):
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

def getBoardByAbbreviation(boardAbbreviation) -> Board:
    """
    Retrieves a board by it's abbreviation.
    Example:
        boardAbbreviation: /g/
    """
    collection = db.mongo[g.DATABASE_NAME]["Boards"]
    result = collection.find_one({'abbreviation': boardAbbreviation})
    if result:
        return Board.from_json(result)
    else:
        return None

def getBoardByCollectionName(collectionName) -> Board:
    """
    Retrieves a board by it's collection name
    Example:
        collectionName: "Board_Technology"
    """
    collection = db.mongo[g.DATABASE_NAME]["Boards"]
    result = collection.find_one({"collection_name": collectionName})
    if result:
        return Board.from_json(result)
    else:
        return None

def checkIfBoardExists(boardCollectionName) -> bool:
    """
    Checks if a board exists and returns a boolean depending on the result
    Example:
        boardCollectionName: "Board_Technology"
    """
    collection = db.mongo[g.DATABASE_NAME]["Boards"]
    result = collection.find_one({"collection_name": boardCollectionName})
    return True if result else False