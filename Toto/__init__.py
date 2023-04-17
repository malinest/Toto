"""
This file is the entry point for the application, it get's called automatically when running "flask run Toto" and contains a single method create_app().
"""

from flask import Flask

#Blueprint imports
from Toto.api.routes import bp_api_index, bp_create_post, bp_create_user, bp_get_user
from Toto.site.routes import bp_index


#Method that get's executed by flask and 
def create_app():
    """
    Creates the flask application and assigns all the blueprints to it
    """
    app = Flask(__name__, static_folder="site/templates/static")

    app.register_blueprint(bp_api_index)
    app.register_blueprint(bp_create_post)
    app.register_blueprint(bp_create_user)
    app.register_blueprint(bp_get_user)
    app.register_blueprint(bp_index)

    return app