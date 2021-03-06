from midi.device import Device, DeviceNotFoundException
from config import Config
from logging import Logger

from threading import Thread  # Should be safe for a small number of devices


class Controller(object):

    def __init__(self, config: Config, logger: Logger):
        self._config = config
        self._devices = list()
        self._threads = list()

        self._logger = logger

    def run(self):

        for name, script_path in self._config.midi_devices:
            try:
                device = Device(name, script_path)
                self._devices.append(device)
                process = Thread(target=device.read)
                process.start()
                self._threads.append(process)
            except DeviceNotFoundException as e:
                print('An exception with a midi device occurred: ')
                print(e)

    def stop(self):
        for device in self._devices:
            device.close()
        #  No way to gracefully stop threads
        return
