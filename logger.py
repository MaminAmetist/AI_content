import logging

logger = logging.getLogger('logger' + __name__)

logger.setLevel(logging.INFO)

_format = logging.Formatter("%(levelname)-10s %(asctime)s %(message)s")

file_handler = logging.FileHandler('parser.log', encoding='utf-8')

file_handler.setFormatter(_format)

logger.addHandler(file_handler)
