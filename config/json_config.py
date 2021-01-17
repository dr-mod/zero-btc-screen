import os
import json


class JsonConfig:
    def __init__(self, file_name=os.path.join(os.path.dirname(__file__), '../configuration.json')):
        self._conf = self._load_screens(file_name)

    def screens(self):
        return self._conf['screens']

    @staticmethod
    def _load_screens(file_name):
        js = open(file_name)
        loaded = json.load(js)

        conf = {}
        for top_key, top_value in loaded.items():
            second_level_conf = {}
            conf[top_key] = second_level_conf
            for iterator in top_value:
                for key, value in iterator.items():
                    second_level_conf[key] = value
        return conf

