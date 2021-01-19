import logging
import sys

from config.config import config

__all__ = ('logger', )


def get_logger():
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    screen_handler = logging.StreamHandler(stream=sys.stdout)
    screen_handler.setFormatter(formatter)
    _logger = logging.getLogger()
    _logger.setLevel(logging.DEBUG if config.logging else logging.NOTSET)
    _logger.addHandler(screen_handler)
    if config.log_file:
        handler = logging.FileHandler('log.txt', mode='w')
        handler.setFormatter(formatter)
        _logger.addHandler(handler)
    return _logger


logger = get_logger()
