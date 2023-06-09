"""
Handles the loading of the config file 
"""

from configparser import ConfigParser
from os.path import exists

config_file_location = "Toto/config.ini"
parser = ConfigParser()

if exists(config_file_location):
    parser.read("Toto/config.ini")
else:
    raise FileNotFoundError("Can't find the config file")

def getConfig(section, parameter):
    """
    Reads a config from the file.
    Example:
        section: Database
        parameter: DATABASE_NAME
    """
    value = parser[section][parameter]
    return value