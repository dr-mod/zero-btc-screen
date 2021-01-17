from config.json_config import JsonConfig
from presentation import screens


class Builder:
    def __init__(self, config: JsonConfig):
        self.config = config

    def bind(self, observable):
        for screen, parameters in self.config.screens().items():
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
            except AttributeError:
                raise BtcConfigError(
                    f'Cannot instantiate {screen}')


class BtcConfigError(Exception):
    """Custom Zero BTC screen Exception"""
