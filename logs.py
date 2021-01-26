import logging
import sys

from config.config import config

__all__ = ('logger', )


def get_logger():
    formatter = logging.Formatter(
        fmt='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S')
    _logger = logging.getLogger()
    if config.console_logs:
        screen_handler = logging.StreamHandler(stream=sys.stdout)
        screen_handler.setFormatter(formatter)
        _logger.addHandler(screen_handler)
        _logger.setLevel(logging.NOTSET)
    if config.logs_file is not None:
        handler = logging.FileHandler(config.logs_file, mode='w')
        handler.setFormatter(formatter)
        _logger.addHandler(handler)
        _logger.setLevel(logging.NOTSET)
    return _logger


logger = get_logger()
