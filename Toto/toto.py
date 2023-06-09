"""
This file is the entry point for the application, it get's called automatically when running "flask run Toto" and contains a single method create_app().
"""

import os
from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

#Blueprint imports
from Toto.api.routes import bp_get_posts, bp_create_post, bp_delete_post, bp_create_board, bp_create_user, bp_get_boards, bp_api_login, bp_create_comment, bp_delete_comment, bp_api_logout
from Toto.site.routes import bp_index, bp_board, bp_post, bp_login, bp_register
import Toto.utils.globals as g

#Method that get's executed by flask and 
def create_app():
    """
    Creates the flask application and assigns all the blueprints to it
    """
    app = Flask(__name__, static_folder="site/templates/static")
    app.config["SECRET_KEY"] = g.SECRET_KEY
    app.config["SESSION_COOKIE_NAME"] = "session"
    limiter = Limiter(get_remote_address, app=app)

    limiter.limit("1 per minute")(bp_create_post)
    limiter.limit("1 per minute")(bp_create_comment)
    limiter.limit("5 per hour")(bp_create_user)

    app.register_blueprint(bp_get_posts)
    app.register_blueprint(bp_get_boards)
    app.register_blueprint(bp_create_post)
    app.register_blueprint(bp_delete_post)
    app.register_blueprint(bp_create_comment)
    app.register_blueprint(bp_delete_comment)
    app.register_blueprint(bp_create_board)
    app.register_blueprint(bp_create_user)
    app.register_blueprint(bp_api_login)
    app.register_blueprint(bp_api_logout)
    app.register_blueprint(bp_index)
    app.register_blueprint(bp_board)
    app.register_blueprint(bp_post)
    app.register_blueprint(bp_login)
    app.register_blueprint(bp_register)

    return app