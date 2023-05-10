"""
Handles all the routes related to the api
"""
import os
import hashlib
from datetime import datetime

from flask import Blueprint, Response, jsonify, request, redirect, url_for
from pymongo.errors import DuplicateKeyError, OperationFailure, CollectionInvalid

import Toto.database.DAO.DAOCounter as DAOCounter
import Toto.database.DAO.DAOUser as DAOUser
import Toto.database.DAO.DAOBoard as DAOBoard
import Toto.database.DAO.DAOPosts as DAOPosts
import Toto.database.db as db
from Toto.models.post import Post
from Toto.models.user import User
from Toto.utils.logs import logger
import Toto.utils.globals as g

ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif"}
ALLOWED_VIDEO_EXTENSIONS = {"mp4"}

#Index
bp_api_index = Blueprint("api_index", __name__, url_prefix="/api")

@bp_api_index.route("/")
def api_index():
    return "<p>This is the access point of the api<p>"

#Get posts
bp_get_posts = Blueprint("get_posts", __name__, url_prefix="/api")

@bp_get_posts.route("/get_posts", methods = ['GET'])
def get_posts():
    board = request.args.get('board')
    if DAOBoard.checkIfBoardExists(board):
        return jsonify(DAOPosts.getAllPostsFromBoard(board))
    else:
        return Response("Board {0} not found".format(board), status=404)

#Create post
bp_create_post = Blueprint("create_post", __name__, url_prefix="/api")

@bp_create_post.route("/create_post", methods = ['POST'])
def create_post():
    board = request.args.get('board')
    if DAOBoard.checkIfBoardExists(board):
        board = DAOBoard.getBoardByCollectionName(board)
        collection = db.mongo[g.DATABASE_NAME][board.collection_name]
        data = request.form
        media = request.files["media"]
        media_fileformat = media.filename.split(".")[-1]
        path = None
        if media:
            if media_fileformat in ALLOWED_IMAGE_EXTENSIONS:
                path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../site/templates/static/images/", media.filename))
            elif media_fileformat in ALLOWED_VIDEO_EXTENSIONS:
                path = os.path.join(os.path.normpath(os.path.join(os.path.dirname(__file__), "../site/templates/static/videos/", media.filename)))
            else:
                return Response("Invalid file format", status=415)
            media.save(path)
        post = Post(DAOCounter.getBoardSequence(board.collection_name), False, data["title"], data["username"], datetime.now(), media.filename, data["content"], [])
        collection.insert_one(post.to_dict())
        logger.info("New post created on {0} with id {1} by {2}".format(board.collection_name, post.id, post.username))
        DAOPosts.deleteLastPostIfOverLimit(board.collection_name)
        return redirect("/{0}/".format(board.abbreviation))
    else:
        return Response("Board {0} not found".format(board.collection_name), status=404)

#Create comment

bp_create_comment = Blueprint("create_comment", __name__, url_prefix="/api")

@bp_create_comment.route("/create_comment", methods = ['POST'])
def create_comment():
    board = request.args.get("board")
    data = request.form
    media = request.files["media"]
    media_fileformat = media.filename.split(".")[-1]
    path = None
    if media:
        if media_fileformat in ALLOWED_IMAGE_EXTENSIONS:
            path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../site/templates/static/images/", media.filename))
        elif media_fileformat in ALLOWED_VIDEO_EXTENSIONS:
            path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../site/templates/static/videos/", media.filename))
        else:
            return Response("Invalid file format", status=415)
        media.save(path)
    post = DAOPosts.getPostByIdOrCommentId(data["id"], board)
    if post:
        comment = {"_id": DAOCounter.getBoardSequence(board), "response_to": data["response_to"], "username": data["username"], "filename": media.filename, "date": datetime.now(), "content": data["content"]}
        collection = db.mongo[g.DATABASE_NAME][board]
        collection.update_one({"_id": post.id}, {"$push": {"comments": comment}})
        logger.info("New comment with id {0} created on {1} by {2}".format(comment["_id"], board, comment["username"]))
        return redirect("/{0}/{1}".format(DAOBoard.getBoardByCollectionName(board).abbreviation, post.id))
    else:
        return Response("There is no post that has or contains this id", status=404)

#Create board
bp_create_board = Blueprint("create_board", __name__, url_prefix="/api")

@bp_create_board.route("/create_board", methods = ['POST'])
def create_board():
    data = request.form
    try:
        db.mongo[g.DATABASE_NAME].create_collection(name="Board_{0}".format(data["board_name"].capitalize()), check_exists=True)
        collection_boards = db.mongo[g.DATABASE_NAME]["Boards"]
        board_data = {"collection_name": "Board_{0}".format(data["board_name"].capitalize()), "name": data["board_name"].capitalize(), "abbreviation": data["abbreviation"].lower()}
        collection_boards.insert_one(board_data)
        collection_counters = db.mongo[g.DATABASE_NAME]["Counters"]
        counter_data = {"collection": "Board_{0}".format(data["board_name"].capitalize()), "sequence": 0}
        collection_counters.insert_one(counter_data)
        return redirect("/{0}/".format(board_data["abbreviation"]))
    except CollectionInvalid:
        return Response("A board with this name already exists", status=409)

#Create user
bp_create_user = Blueprint("create_user", __name__, url_prefix="/api")

@bp_create_user.route("/create_user", methods = ['POST'])
def create_user():
    collection = db.mongo[g.DATABASE_NAME]["Users"]
    if len(request.form["password"]) < 8:
        return Response("Invalid password length, the password must be at least 8 characters long", status=400)
    try:
        salt = os.urandom(16)
        user = User(request.form["username"], request.form["email"], hashlib.sha256(request.form["password"].encode("utf-8") + salt).digest(), salt, False, datetime.now())
        collection.insert_one(user.to_dict())
        logger.info("New user {0} created".format(user.username))
        return redirect("/user/login")
    except DuplicateKeyError:
        return Response("Username {0} already exists".format(user.username), status=400)

#Login
bp_api_login = Blueprint("api_login", __name__, url_prefix="/api")

@bp_api_login.route("/login", methods = ['POST'])
def api_login():
    collection = db.mongo[g.DATABASE_NAME]["Users"]
    user = DAOUser.getUserByUsername(request.form["username"])
    if user:
        if user.password == hashlib.sha256(request.form["password"].encode("utf-8") + user.salt).digest():
            return redirect("/")
        else:
            return Response("Invalid password for user {0}".format(user.username), status=401)
    return Response("The user {0} doesn't exist".format(request.form["username"]), status=401)