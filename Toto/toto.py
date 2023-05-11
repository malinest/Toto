"""
This file is the entry point for the application, it get's called automatically when running "flask run Toto" and contains a single method create_app().
"""

import os
from flask import Flask

#Blueprint imports
from Toto.api.routes import bp_api_index, bp_get_posts, bp_create_post, bp_delete_post, bp_create_board, bp_create_user, bp_api_login, bp_create_comment
from Toto.site.routes import bp_index, bp_board, bp_post, bp_login, bp_register


#Method that get's executed by flask and 
def create_app():
    """
    Creates the flask application and assigns all the blueprints to it
    """
    app = Flask(__name__, static_folder="site/templates/static")
    app.secret_key = os.urandom(12).hex()

    app.register_blueprint(bp_api_index)
    app.register_blueprint(bp_get_posts)
    app.register_blueprint(bp_create_post)
    app.register_blueprint(bp_delete_post)
    app.register_blueprint(bp_create_comment)
    app.register_blueprint(bp_create_board)
    app.register_blueprint(bp_create_user)
    app.register_blueprint(bp_api_login)
    app.register_blueprint(bp_index)
    app.register_blueprint(bp_board)
    app.register_blueprint(bp_post)
    app.register_blueprint(bp_login)
    app.register_blueprint(bp_register)

    return app