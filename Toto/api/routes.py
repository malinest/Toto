"""
Handles all the routes relates to the api
"""

from flask import Blueprint, request, Response

import Toto.database.db as db
from Toto.utils.logs import logger

#Index
bp_index = Blueprint("index", __name__, url_prefix="/api")

@bp_index.route("/")
def index():
    return "<p>This is the access point of the api<p>"

#Create Post
bp_create_post = Blueprint("create_post", __name__, url_prefix="/api")

@bp_create_post.route("/create_post", methods = ['POST'])
def create_post():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        return json
    else:
        logger.warning('Invalid post content type!')
        return Response("Error 400: Bad request\n", status=400)