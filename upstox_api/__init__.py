import logging
import os

_logger = logging.getLogger('websocket')
_logger.addHandler(logging.NullHandler())

logging.getLogger(__name__).addHandler(logging.StreamHandler())
LOG_LEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logging._checkLevel(LOG_LEVEL)
logging.getLogger(__name__).setLevel(LOG_LEVEL)
logger = logging.getLogger("upstox_api")
logger.debug("Log Level :: %s", LOG_LEVEL)