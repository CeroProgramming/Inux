from configparser import ConfigParser
from os.path import isfile
from typing import List, Tuple
from logging import Logger

Keyboards = List[Tuple[str, str]]
MIDIDevices = List[Tuple[str, str]]


class NoValidConfig(Exception):
    pass


class Config(object):

    def __init__(self, config_fp: str, logger: Logger):

        if not config_fp:
            raise NoValidConfig('No config passed. Use flag --config <fp>.')
        if not isfile(config_fp):
            raise NoValidConfig('Passed file "%s" not found..' % (config_fp,))

        self._config = ConfigParser()
        self._config.read(config_fp)
        self._logger = logger

    @property
    def devices(self) -> Keyboards:
        devices = list()
        for section in self._config.sections():
            device_type = self._config[section].get('type')
            if device_type == 'device':
                self._logger.info('Found config section for device "%s"' % (section,))
                script_path = self._config[section].get('script')
                if script_path:
                    self._logger.info('Registered device!')
                    devices.append((section, script_path))
                else:
                    self._logger.info('Config is missing the "script" attribute')
                    continue
        return devices

    @property
    def midi_devices(self) -> MIDIDevices:
        devices = list()
        for section in self._config.sections():
            self._logger.info('Found config section for midi device "%s"' % (section,))
            device_type = self._config[section].get('type')
            if device_type == 'midi':
                script_path = self._config[section].get('script')
                if script_path:
                    self._logger.info('Registered midi device!')
                    devices.append((section, script_path))
                else:
                    self._logger.info('Config is missing the "script" attribute')
                    continue
        return devices
