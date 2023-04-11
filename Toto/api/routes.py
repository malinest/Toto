from flask import Blueprint

import Toto.database.db as db

#Index
bp_index = Blueprint("index", __name__, url_prefix="/api")

@bp_index.route("/")
def index():
    return "<p>This is the access point of the api<p>"