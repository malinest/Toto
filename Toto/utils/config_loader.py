from configparser import ConfigParser
from os.path import exists

config_file_location = "Toto/config.ini"
parser = ConfigParser()

if exists(config_file_location):
    parser.read("Toto/config.ini")
else:
    raise FileNotFoundError("Can't find the config file")

def getConfig(section, parameter):
    value = parser[section][parameter]
    return value