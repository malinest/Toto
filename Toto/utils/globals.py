"""
This file stores most of the global variables of the aplication, most of wich are loaded from the config file.
"""

import Toto.utils.config_loader as config_loader

DATABASE_URL = config_loader.getConfig("Database", "URL")