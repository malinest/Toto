"""

This file is the entry point for the application, it get's called automatically when running "flask run Toto" and contains a single method create_app().

"""

from flask import Flask
import Toto.database.db as db
import Toto.utils.config_loader as config

#Blueprint imports
from Toto.api.routes import bpindex

#Method that get's executed by flask and 
def create_app():
    """
    Creates the flask application and assigns all the blueprints to it
    """
    app = Flask(__name__)

    config.getAllConfigs()

    app.register_blueprint(bpindex)

    return app