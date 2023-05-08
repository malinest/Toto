"""
DAO for the posts collections
"""

import Toto.database.db as db
from Toto.models.post import Post
from Toto.utils.logs import logger
import Toto.utils.globals as g
import Toto.database.DAO.DAOBoard as DAOBoard

def getAllPostsFromBoard(board):
    """
    Retrieves all posts from a specified board by it's name
    Example: Board_Technology
    """
    posts = []
    collection = db.mongo[g.DATABASE_NAME][board]
    result = collection.find({})
    for post in result:
        oPost = Post.from_json(post)
        if oPost.is_pinned:
            posts.insert(0, oPost)
        else:
            posts.append(oPost)
    logger.debug("Recieved {0} posts from {1}".format(len(posts), board))
    return posts

def getRandomPosts():
    """
    Function that returns 8 random posts from different boards to be displayed on the main page
    """
    posts = {}
    pipeline = [
        {"$sample": {"size": 1}}
    ]
    database = db.mongo[g.DATABASE_NAME]
    for board, i in zip(DAOBoard.getAllBoards(), range(8)):
        collection = database[board.collection_name]
        results = collection.aggregate(pipeline)
        for result in results:
            posts[board.abbreviation] = Post.from_json(result)
    return posts

def getPostById(id, board):
    """
    Function that retrieves a post by it's id
    Input example: 50, Board_Technology
    """
    collection = db.mongo[g.DATABASE_NAME][board]
    result = collection.find_one({"_id": int(id)})
    if result:
        return Post.from_json(result)
    else:
        return None

def getPostByCommentId(comment_id, board):
    """
    Function that retrieves a post by a comment's id
    Input example: 50, Board_Technology
    """
    collection = db.mongo[g.DATABASE_NAME][board]
    result = collection.find_one({"comments._id": int(comment_id)})
    if result:
        return Post.from_json(result)
    else:
        return None

def getPostByIdOrCommentId(id, board):
    """
    Function that retrieves a post by an id, the id can be of the post or of one of the post's comments
    Input example: 50, Board_Technology
    """
    collection = db.mongo[g.DATABASE_NAME][board]
    result_post = collection.find_one({"_id": int(id)})
    if result_post:
        return Post.from_json(result_post)
    result_comment = collection.find_one({"comments._id": int(id)})
    if result_comment:
        return Post.from_json(result_comment)
    else:
        return None

def deleteLastPostIfOverLimit(board):
    """
    Function that checks if a board has over 100 posts and deletes the older ones
    Input example: Board_Technology
    """
    collection = db.mongo[g.DATABASE_NAME][board]
    number_of_posts = collection.count_documents({})
    if number_of_posts >= 100:
        collection.delete_one({"is_pinned": False})
        logger.debug("Deleted last post from {0}".format(board))