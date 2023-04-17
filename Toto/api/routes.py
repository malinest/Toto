"""
Handles all the routes relates to the api
"""
from datetime import datetime
from flask import Blueprint, request, Response
from pymongo.errors import OperationFailure
from PIL import Image
import io

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

        im = Image.open(json["image"])
        image_bytes = io.BytesIO()
        im.save(image_bytes, format('JPEG'))

        database = db.mongo["TotoDB"]
        collection = database[board]
        collection.insert_one(json)
        logger.info("New post created on {0}".format(board))
        return Response("Post created successfully", status=201)
    else:
        logger.warning('Invalid request content type')
        return Response("Invalid request content type", status=400)

#Create User
bp_create_user = Blueprint("create_user", __name__, url_prefix="/api")

@bp_create_user.route("/create_user", methods = ['POST'])
def create_user():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        json["date"] = datetime.now()
        database = db.mongo["TotoDB"]
        collection = database["Users"]
        collection.insert_one(json)
        logger.info("New user created on {0}".format('users'))
        return Response("User created successfully\n", status=201)
    else:
        logger.warning('Invalid request content type')
        return Response("Invalid request content type", status=400)

#Get User
bp_get_user = Blueprint("get_user", __name__, url_prefix="/api")

@bp_get_user.route("/get_user", methods = ['GET'])
def get_user():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        database = db.mongo["TotoDB"]
        collection = database["Users"]
        result = collection.find_one({'username': json['username'], 'pwd': json['pwd']})
        logger.info("Request for user on {0}".format('Users'))
        logger.debug(result)
        if result:
            return Response('Found!\n', status=302)
        else:
            return Response('Not Found\n', status=404)
    else:
        logger.warning('Invalid request content type')
        return Response("Invalid request content type\n", status=400)