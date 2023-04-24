"""
Handles all the routes relates to the api
"""
import base64
from datetime import datetime

from flask import Blueprint, Response, jsonify, request
from pymongo.errors import DuplicateKeyError, OperationFailure

import Toto.database.DAO.DAOCounter as DAOCounter
import Toto.database.DAO.DAOUser as DAOUser
import Toto.database.DAO.DAOBoard as DAOBoard
import Toto.database.db as db
from Toto.models.post import Post
from Toto.models.user import User
from Toto.utils.logs import logger
import Toto.utils.globals as g

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
        collection = db.mongo[g.DATABASE_NAME][board]
        data = request.form
        post = Post(DAOCounter.getBoardSequence(board), data["title"], data["username"], datetime.now(), base64.b64encode(request.files["media"].read()), request.files["media"].filename, data["content"], [])
        collection.insert_one(post.to_dict())
        logger.info("New post created on {0} with id {1} by {2}".format(board, post.id, post.username))
        return Response("Post created successfully", status=201)
    else:
        return Response("Board not found", status=404)

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