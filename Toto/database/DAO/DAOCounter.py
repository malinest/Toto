import Toto.database.db as db
from Toto.models.counter import Counter
import Toto.utils.globals as g

def getBoardSequence(board):
    """
    Returns the current sequience of a board's counter and increases it by 1
    Input example: Board_Technology
    """
    collection = db.mongo["TotoDB"]["Counters"]
    increaseBoardCounter(board)
    result = collection.find_one({"collection": board})
    counter = Counter.from_json(result)
    return counter.sequence

def increaseBoardCounter(board):
    """
    Increases a board's counter by 1
    Input example: Board_Technology
    """
    collection = db.mongo["TotoDB"]["Counters"]
    collection.update_one({"collection": board}, {"$inc": {"sequence": 1}})