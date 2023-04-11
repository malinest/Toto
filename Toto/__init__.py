"""
This file is the entry point for the application, it get's called automatically when running "flask run Toto" and contains a single method create_app().
"""

from flask import Flask

#Blueprint imports
from Toto.api.routes import bp_index, bp_create_post


#Method that get's executed by flask and 
def create_app():
    """
    Creates the flask application and assigns all the blueprints to it
    """
    app = Flask(__name__)

    app.register_blueprint(bp_index)
    app.register_blueprint(bp_create_post)

    return app