"""
Handles all the routes relates to the api
"""
from datetime import datetime
from io import BytesIO

from flask import Blueprint, Response, jsonify, request
from pymongo.errors import OperationFailure

import Toto.database.db as db
from Toto.utils.logs import logger
from Toto.models.user import User

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
    collection = db.mongo["TotoDB"]["Users"]
    user = User(request.form["username"], request.form["email"], request.form["password"], request.form["birthday"], BytesIO(request.files["profile_picture"].read()), datetime.now())
    logger.info("New user creater")
    return Response(str(user), status=201)

#Get User
bp_get_user = Blueprint("get_user", __name__, url_prefix="/api")

@bp_get_user.route("/get_user", methods = ['GET'])
def get_user():
#    content_type = request.headers.get('Content-Type')
#    if (content_type == 'application/json'):
#        json = request.json
#        database = db.mongo["TotoDB"]
#        collection = database["Users"]
#        result = collection.find_one({'username': json['username']})
#        logger.info("Request for user on {0}".format('Users'))
#        logger.debug(result)
#        if result:
#            if bcrypt.check_password_hash(result['pwd'], json['pwd']):
#                logger.debug(msg)('Log in successful')
#                return Response('Log in successful!\n', status=302)
#            else:
#                logger.debug(msg)('Password not matching')
#                return Response("Username and password doesn't match\n", status=404)
#        else:
#            logger.info('User not found')
#            return Response("User not found\n", status=404)
#    else:
#        logger.warning('Invalid request content type')
#        return Response("Invalid request content type\n", status=400)
    return None