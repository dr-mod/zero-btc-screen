import configparser
import os

__all__ = ('config', 'Config')


class Config:
    def __init__(self, file_name=os.path.join(os.path.dirname(__file__), os.pardir, 'configuration.cfg')):
        self._conf = self._load_screens(file_name)

    @property
    def console_logs(self):
        return self._conf.getboolean('base', 'console_logs', fallback=False)

    @property
    def logs_file(self):
        return self._conf.get('base', 'logs_file', fallback=None)

    @property
    def dummy_data(self):
        return self._conf.getboolean('base', 'dummy_data', fallback=False)

    @property
    def screens(self):
        screens = self._conf.get('base', 'screens', fallback='').strip('[]\n').split('\n')
        screens_conf = {}
        for screen in screens:
            screens_conf[screen] = dict(self._conf.items(screen))
        return screens_conf

    @property
    def refresh_interval(self):
        return self._conf.getint('base', 'refresh_interval_minutes', fallback=15) * 60

    @property
    def currency(self):
        return self._conf.get('base', 'currency', fallback='BTC')

    @staticmethod
    def _load_screens(file_name):
        conf = configparser.ConfigParser()
        conf.read_file(open(file_name))
        return conf


# we want to import the config across the files
config = Config()
