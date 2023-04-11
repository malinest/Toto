from flask import Blueprint, request, Response
from pymongo.errors import OperationFailure

import Toto.database.db as db
from Toto.utils.logs import logger

#Index
bp_index = Blueprint("index", __name__, url_prefix="/api")

@bp_index.route("/")
def index():
    return "<p>This is the access point of the api<p>"

#Create Post
#TODO: Check if the collection's name (board)
bp_create_post = Blueprint("create_post", __name__, url_prefix="/api")

@bp_create_post.route("/create_post", methods = ['POST'])
def create_post():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        board = request.args.get('board')
        json = request.json
        database = db.mongo["TotoDB"]
        collection = database[board]
        collection.insert_one(json)
        return "Inserted successfully!\n"
    else:
        logger.warning('Invalid post content type!')
        return Response("Error 400: Bad request\n", status=400)