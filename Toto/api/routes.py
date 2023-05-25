"""
Handles all the routes related to the api
"""
import os
import hashlib
import random
from datetime import datetime

from flask import Blueprint, Response, jsonify, request, redirect, url_for, session, flash
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

#Get boards
bp_get_boards = Blueprint("get_boards", __name__, url_prefix="/api")

@bp_get_boards.route("/get_boards", methods = ['GET'])
def get_boards():
    """
    Returns a json with all the boards.
    """
    return jsonify(DAOBoard.getAllBoards())

#Get posts
bp_get_posts = Blueprint("get_posts", __name__, url_prefix="/api")

@bp_get_posts.route("/get_posts", methods = ['GET'])
def get_posts():
    """
    Returns a json with all the posts from a board.
    Required url args: 'board' (name of the collection).
    """
    board = request.args.get('board')
    if DAOBoard.checkIfBoardExists(board):
        return jsonify(DAOPosts.getAllPostsFromBoard(board))
    else:
        return Response("Board {0} not found".format(board), status=404)

#Create post
bp_create_post = Blueprint("create_post", __name__, url_prefix="/api")

@bp_create_post.route("/create_post", methods = ['POST'])
def create_post():
    """
    Creates a post in the desired board.
    Required url args: 'board' (name of the collection).
    Required html form parameters: username, title, content and a file named 'media'.
    """
    board = request.args.get('board')
    if DAOBoard.checkIfBoardExists(board):
        board = DAOBoard.getBoardByCollectionName(board)
        collection = db.mongo[g.DATABASE_NAME][board.collection_name]
        data = request.form
        media = request.files["media"]
        media_fileformat = media.filename.split(".")[-1]
        generated_filename = ''
        path = None
        if media:
            generated_filename = "{0}.{1}".format(str(random.randint(10_000_000, 99_999_999)), media_fileformat)
            if media_fileformat in g.ALLOWED_IMAGE_EXTENSIONS:
                path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../site/templates/static/images/", generated_filename))
            elif media_fileformat in g.ALLOWED_VIDEO_EXTENSIONS:
                path = os.path.join(os.path.normpath(os.path.join(os.path.dirname(__file__), "../site/templates/static/videos/", generated_filename)))
            else:
                return Response("Invalid file format", status=415)
            media.save(path)
        post = Post(DAOCounter.getBoardSequence(board.collection_name), False, data["title"], data["username"], datetime.now(), generated_filename, data["content"], [])
        collection.insert_one(post.to_dict())
        logger.info("New post created on {0} with id {1} by {2}".format(board.collection_name, post.id, post.username))
        DAOPosts.deleteLastPostIfOverLimit(board.collection_name)
        return redirect("/{0}/".format(board.abbreviation))
    else:
        return Response("Board {0} not found".format(board.collection_name), status=404)

#Delete post
bp_delete_post = Blueprint("delete_post", __name__, url_prefix="/api")

@bp_delete_post.route("/delete_post", methods = ['GET'])
def delete_post():
    """
    Deletes a post by it's id from the specified board.
    Required url args: 'board' (name of the collection), 'post_id'.
    WARNING: Requires admin permissions.
    """
    board = request.args.get("board")
    board = DAOBoard.getBoardByCollectionName(board)
    post_id = request.args.get("post_id")
    if session['is_admin']:
        if DAOBoard.checkIfBoardExists(board.collection_name):
            if DAOPosts.deletePostById(post_id, board.collection_name):
                logger.info("Deleted post with id {0} in {1}".format(post_id, board.collection_name))
                return redirect("/{0}/".format(board.abbreviation))
            else:
                return Response("Couldn't delete the post {0}".format(post_id), status=404)
        else:
            return Response("Board {0} not found".format(board.collection_name), status=404)
    else:
        return Response("You don't enough permissions to delete posts", status=403)

#Create comment
bp_create_comment = Blueprint("create_comment", __name__, url_prefix="/api")

@bp_create_comment.route("/create_comment", methods = ['POST'])
def create_comment():
    """
    Creates a comment under the the desired post.
    Required url args: 'board' (name of the collection).
    Required html form parameters: id (this is the id of the post we want to comment under), response_to, username, content and a file named 'media'.
    """
    board = request.args.get("board")
    data = request.form
    media = request.files["media"]
    media_fileformat = media.filename.split(".")[-1]
    path = None
    generated_filename = ''
    if media:
        generated_filename = "{0}.{1}".format(str(random.randint(10_000_000, 99_999_999)), media_fileformat)
        if media_fileformat in g.ALLOWED_IMAGE_EXTENSIONS:
            path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../site/templates/static/images/", generated_filename))
        elif media_fileformat in g.ALLOWED_VIDEO_EXTENSIONS:
            path = os.path.normpath(os.path.join(os.path.dirname(__file__), "../site/templates/static/videos/", generated_filename))
        else:
            return Response("Invalid file format", status=415)
        media.save(path)
    post = DAOPosts.getPostByIdOrCommentId(data["id"], board)
    if post:
        comment = {"_id": DAOCounter.getBoardSequence(board), "response_to": data["response_to"], "username": data["username"], "filename": generated_filename, "date": datetime.now(), "content": data["content"]}
        collection = db.mongo[g.DATABASE_NAME][board]
        collection.update_one({"_id": post.id}, {"$push": {"comments": comment}})
        logger.info("New comment with id {0} created on {1} by {2}".format(comment["_id"], board, comment["username"]))
        return redirect("/{0}/{1}".format(DAOBoard.getBoardByCollectionName(board).abbreviation, post.id))
    else:
        return Response("There is no post that has or contains this id", status=404)

#Delete comment
bp_delete_comment = Blueprint("delete_comment", __name__, url_prefix="/api")

@bp_delete_comment.route("/delete_comment", methods = ['GET'])
def delete_comment():
    """
    Deletes a comment by it's id and the parent's post id
    Required url args: 'board' (name of the collection), 'comment_id', 'post_id'.
    WARNING: Requires admin permissions.
    """
    board = request.args.get("board")
    board = DAOBoard.getBoardByCollectionName(board)
    post_id = request.args.get("post_id")
    comment_id = request.args.get("comment_id")
    if session['is_admin']:
        if DAOBoard.checkIfBoardExists(board.collection_name):
            if DAOPosts.deleteCommentById(comment_id, post_id, board.collection_name):
                logger.info("Deleted comment with id {0} on post {1} in {2}".format(comment_id, post_id, board.collection_name))
                return redirect("/{0}/{1}".format(board.abbreviation, post_id))
            else:
                return Response("Couldn't delete the comment {0}".format(post_id), status=404)
        else:
            return Response("Board {0} not found".format(board.collection_name), status=404)
    else:
        return Response("You don't enough permissions to delete comments", status=403)

#Create board
bp_create_board = Blueprint("create_board", __name__, url_prefix="/api")

@bp_create_board.route("/create_board", methods = ['POST'])
def create_board():
    """
    Creates a new board.
    Required html form parameters: board_name, abbreviation.
    WARNING: Requires admin permissions.
    """
    if session['is_admin']:
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
    else:
        return Response("You don't have permissions to delete create boards", status=403)

#Create user
bp_create_user = Blueprint("create_user", __name__, url_prefix="/api")

@bp_create_user.route("/create_user", methods = ['POST'])
def create_user():
    """
    Creates a new user.
    Required html form parameters: username, email, password.
    """
    collection = db.mongo[g.DATABASE_NAME]["Users"]
    if len(request.form["password"]) < 8:
        return Response("Invalid password length, the password must be at least 8 characters long", status=400)
    try:
        salt = os.urandom(16)
        user = User(request.form["username"], request.form["email"], hashlib.sha256(request.form["password"].encode("utf-8") + salt).digest(), salt, False, datetime.now())
        collection.insert_one(user.to_dict())
        logger.info("New user {0} created".format(user.username))
        flash("User created successfully")
        return redirect("/user/login")
    except DuplicateKeyError:
        return Response("Username {0} already exists".format(user.username), status=400)

#Login
bp_api_login = Blueprint("api_login", __name__, url_prefix="/api")

@bp_api_login.route("/login", methods = ['POST'])
def api_login():
    """
    Checks an user's password and creates his session.
    Required html form parameters: username, password
    """
    collection = db.mongo[g.DATABASE_NAME]["Users"]
    user = DAOUser.getUserByUsername(request.form["username"])
    if user:
        if user.password == hashlib.sha256(request.form["password"].encode("utf-8") + user.salt).digest():
            session["user"] = user.username
            session["is_admin"] = user.is_admin
            session.permanent = True
            return redirect("/")
        else:
            return Response("Invalid password for user {0}".format(user.username), status=401)
    return Response("The user {0} doesn't exist".format(request.form["username"]), status=401)

#Logout
bp_api_logout = Blueprint("api_logout", __name__, url_prefix="/api")

@bp_api_logout.route("/logout", methods = ['GET'])
def api_logout():
    """
    Clears an user's session.
    """
    if "user" in session.keys():
        session.clear()
        return redirect("/")
    else:
        return "You are not logged in"
