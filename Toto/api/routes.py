"""
Handles all the routes relates to the api
"""
from datetime import datetime
from flask import Blueprint, request, Response
from pymongo.errors import OperationFailure

import Toto.database.db as db
from Toto.utils.logs import logger

#Index
bp_api_index = Blueprint("api_index", __name__, url_prefix="/api")

@bp_api_index.route("/")
def api_index():
    return "<p>This is the access point of the api<p>"

#Create Post
#TODO: Check if the collection's name (board)
bp_create_post = Blueprint("create_post", __name__, url_prefix="/api")

@bp_create_post.route("/create_post", methods = ['POST'])
def create_post():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        board = request.args.get('board')
        board = "Board_{}".format(board)
        json = request.json
        json["date"] = datetime.now()
        database = db.mongo["TotoDB"]
        collection = database[board]
        collection.insert_one(json)
        logger.info("New post created on {0}", board)
        return Response("Post created successfully", status=201)
    else:
        logger.warning('Invalid post content type')
        return Response("Invalid request content type", status=400)