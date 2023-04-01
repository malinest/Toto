import logging

import Toto.utils.globals as g

logger = logging.getLogger(__name__)

log_format = logging.Formatter(fmt = "%(levelname)s %(asctime)s: %(message)s", datefmt="%d:%m:%Y %H:%M:%S")

file_handler = logging.FileHandler("{0}".format(g.LOG_FILE))
file_handler.setFormatter(log_format)
file_handler.setLevel(logging.ERROR)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
if g.LOG_LEVEL == "DEBUG":
    console_handler.setLevel(logging.DEBUG)
    logger.setLevel(logging.DEBUG)
elif g.LOG_LEVEL == "INFO":
    console_handler.setLevel(logging.INFO)
    logger.setLevel(logging.INFO)
elif g.LOG_LEVEL == "WARNING":
    console_handler.setLevel(logging.WARNING)
    logger.setLevel(logging.WARNING)
elif g.LOG_LEVEL == "ERROR":
    console_handler.setLevel(logging.ERROR)
    logger.setLevel(logging.ERROR)
elif g.LOG_LEVEL == "CRITICAL":
    console_handler.setLevel(logging.CRITICAL)
    logger.setLevel(logging.CRITICAL)
else:
    console_handler.setLevel(logging.CRITICAL)
    logger.setLevel(logging.CRITICAL)
console_handler.setFormatter(log_format)
logger.addHandler(console_handler)