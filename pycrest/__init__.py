import logging


class NullHandler(logging.Handler):
    def emit(self, record):
        pass

logger = logging.getLogger('pycrest')
logger.addHandler(NullHandler())

version = "0.1.0"

from .eve import EVE