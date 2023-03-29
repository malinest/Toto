from flask import Blueprint

#Index
bpindex = Blueprint("index", __name__)

@bpindex.route("/")
def index():
    return "<h1>It's working!</h1>"