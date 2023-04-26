"""
Handles all the routes related to the api
"""
import base64
import os
from datetime import datetime

from flask import Blueprint, Response, jsonify, request, redirect, url_for
from pymongo.errors import DuplicateKeyError, OperationFailure, CollectionInvalid

import Toto.database.DAO.DAOCounter as DAOCounter
import Toto.database.DAO.DAOUser as DAOUser
import Toto.database.DAO.DAOBoard as DAOBoard
import Toto.database.db as db
from Toto.models.post import Post
from Toto.models.user import User
from Toto.utils.logs import logger
import Toto.utils.globals as g

ALLOWED_EXTENSIONS = {".jpg", "jpeg", ".png", ".gif", ".mp4", ".mkv"}

#Index
bp_api_index = Blueprint("api_index", __name__, url_prefix="/api")

@bp_api_index.route("/")
def api_index():
    return "<p>This is the access point of the api<p>"

#Create Post
bp_create_post = Blueprint("create_post", __name__, url_prefix="/api")

@bp_create_post.route("/create_post", methods = ['POST'])
def create_post():
    board = request.args.get('board')
    if DAOBoard.checkIfBoardExists(board):
        board = DAOBoard.getBoardByCollectionName(board)
        collection = db.mongo[g.DATABASE_NAME][board.collection_name]
        data = request.form
        media = request.files["media"]
        #if os.path.splitext(media.filename)[1] in ALLOWED_EXTENSIONS:
        post = Post(DAOCounter.getBoardSequence(board.collection_name), data["title"], data["username"], datetime.now(), base64.b64encode(media.read()), request.files["media"].filename, data["content"], [])
        collection.insert_one(post.to_dict())
        logger.info("New post created on {0} with id {1} by {2}".format(board.collection_name, post.id, post.username))
        return redirect("/{0}/".format(board.abbreviation), code=201)
        #else:
        #    return Response("Invalid file extension", status=415)
    else:
        return Response("Board not found", status=404)

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
        return Response("Board created successfully", status=201)
    except CollectionInvalid:
        return Response("A board with this name already exists", status=409)

#Create User
bp_create_user = Blueprint("create_user", __name__, url_prefix="/api")

@bp_create_user.route("/create_user", methods = ['POST'])
def create_user():
    collection = db.mongo[g.DATABASE_NAME]["Users"]
    user = User(request.form["username"], request.form["email"], request.form["password"], request.form["birthday"], BytesIO(request.files["profile_picture"].read()), datetime.now())
    try:
        collection.insert_one(user.to_dict())
        logger.info("New user {0} created".format(user.username))
        return Response("User {0} created successfully".format(user.username), status=201)
    except DuplicateKeyError:
        return Response("Username {0} already exists".format(user.username), status=400)


#Login
bp_login = Blueprint("login", __name__, url_prefix="/api")

@bp_login.route("/login", methods = ['POST'])
def login():
    collection = db.mongo[g.DATABASE_NAME]["Users"]
    user = DAOUser.getUserByUsername(request.form["username"])
    if user.password == request.form["password"]:
        return Response("Logged in successfully", status=200)
    else:
        return Response("Loggin incorrect", status=401)