from configparser import ConfigParser
from os.path import isfile
from typing import List

Keyboards = List[str]


class NoValidConfig(Exception):
    pass


class Config(object):

    def __init__(self, config_fp):

        if not config_fp:
            raise NoValidConfig('No config passed. Use flag --config <fp>.')
        if not isfile(config_fp):
            raise NoValidConfig('Passed file "%s" not found..' % (config_fp,))

        self._config = ConfigParser()
        self._config.read(config_fp)

    def get_keyboards(self) -> Keyboards:
        return self._config['DEFAULT']['keyboards'].split(',')
