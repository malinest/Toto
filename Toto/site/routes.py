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
    collection = db.mongo[g.DATABASE_NAME]["Boards"]
    boards = DAOBoard.getAllBoards()
    return render_template("index.html", boards=boards, result=200)

#Boards
bp_board = Blueprint("board", __name__, template_folder="templates/")

@bp_board.route("/<board>/", methods=['GET'])
def board(board):
    full_board = DAOBoard.getBoardByAbbreviation(board)
    posts = DAOPosts.getAllPostsFromBoard(full_board.collection_name)
    return render_template("board.html", board=full_board, posts=posts, result=200)