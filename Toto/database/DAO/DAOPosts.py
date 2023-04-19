"""
DAO for the posts collections
"""

import json
import Toto.database.db as db
from Toto.utils.logs import logger

def getAllPostsFromBoard(board):
    """
    Retrieves all posts from a specified board by it's name
    Example: Board_Technology
    """
    posts = []
    collection = db.mongo["TotoDB"][board]
    result = collection.find({})
    for post in result:
        posts.append(Post.from_json(post))
    logger.debug("Recieved {0} posts from {1}".format(len(posts), board))
    return posts