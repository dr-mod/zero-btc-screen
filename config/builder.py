from config.config import Config
from logs import logger
from presentation import screens


class Builder:
    def __init__(self, config: Config):
        logger.info('Building up')
        self.config = config

    def bind(self, observable):
        for screen, parameters in self.config.screens.items():
            logger.info(f'Binding {screen}')
            try:
                kwargs = {}
                package = getattr(screens, screen.lower())
                screen_class = getattr(package, screen.lower().capitalize())
                init_varnames = screen_class.__init__.__code__.co_varnames
                for argument in init_varnames:
                    screen_config_value = parameters.get(argument)
                    if screen_config_value is not None:
                        kwargs[argument] = screen_config_value
                screen_class(observable=observable, **kwargs)
                logger.info(f'{screen} initialized')
            except AttributeError as e:
                logger.error(str(e))
                raise BtcConfigError(
                    f'Cannot instantiate {screen}')


class BtcConfigError(Exception):
    """Custom Zero BTC screen Exception"""
