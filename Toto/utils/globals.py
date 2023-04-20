"""
Stores most of the global variables of the aplication, most of wich are loaded from the config file.
"""

import Toto.utils.config_loader as config_loader

#Database variables
DATABASE_URL = config_loader.getConfig("Database", "URL")
DATABASE_NAME = config_loader.getConfig("Database", "DATABASE_NAME")

#Logging
LOG_LEVEL = config_loader.getConfig("Logging", "LOG_LEVEL")
LOG_FILE = config_loader.getConfig("Logging", "LOG_FILE")
LOG_FOLDER = config_loader.getConfig("Logging", "LOG_FOLDER")