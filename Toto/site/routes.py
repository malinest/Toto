"""
Handles all the routes relates to the site
"""

import os
from flask import Blueprint, render_template, url_for
from pymongo.errors import OperationFailure

import Toto.database.db as db
import Toto.database.DAO.DAOBoard as DAOBoard
from Toto.utils.logs import logger

#Index
bp_index = Blueprint("index", __name__, template_folder="templates/")

@bp_index.route("/")
def index():
    collection = db.mongo["TotoDB"]["Boards"]
    boards = DAOBoard.getAllBoards()
    return render_template("index.html", boards=boards, result = 200)