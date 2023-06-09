"""
Handles all the routes relates to the site
"""

import os
from flask import Blueprint, render_template, url_for
from pymongo.errors import OperationFailure

import Toto.database.db as db
import Toto.database.DAO.DAOBoard as DAOBoard
import Toto.database.DAO.DAOPosts as DAOPosts
from Toto.utils.logs import logger
import Toto.utils.globals as g

#Index
bp_index = Blueprint("index", __name__, template_folder="templates/")

@bp_index.route("/", methods=['GET'])
def index():
    """
    Renders index.html
    """
    collection = db.mongo[g.DATABASE_NAME]["Boards"]
    boards = DAOBoard.getAllBoards()
    posts = DAOPosts.getTrendingPosts()
    return render_template("index.html", boards=boards, posts=posts, result=200)

#Boards
bp_board = Blueprint("board", __name__, template_folder="templates/")

@bp_board.route("/<board>/", methods=['GET'])
def board(board):
    """
    Renders board.html with the specified board
    Example:
        board: Board_Technology
    """
    full_board = DAOBoard.getBoardByAbbreviation(board)
    posts = DAOPosts.getAllPostsFromBoard(full_board.collection_name)
    return render_template("board.html", board=full_board, posts=posts, result=200)

#Posts
bp_post = Blueprint("post", __name__, template_folder="templates/")

@bp_post.route("/<board>/<post_id>", methods=['GET'])
def post(board, post_id):
    """
    Renders post.html with the specified post
    Example:
        board: Board_Technology
        post_id: 13
    """
    full_board = DAOBoard.getBoardByAbbreviation(board)
    post = DAOPosts.getPostById(post_id, full_board.collection_name)
    return render_template("post.html", post=post, board=full_board)

#Login
bp_login = Blueprint("login", __name__, template_folder="templates/", url_prefix="/user")

@bp_login.route("/login", methods = ['GET'])
def login():
    """
    Renders login.html
    """
    return render_template("login.html")

#Register
bp_register = Blueprint("register", __name__, template_folder="templates/", url_prefix="/user")

@bp_register.route("/register", methods = ['GET'])
def register():
    """
    Renders register.html
    """
    return render_template("register.html")