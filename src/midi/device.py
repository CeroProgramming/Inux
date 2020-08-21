from time import sleep
from typing import List
from importlib import import_module
from multiprocessing import Process
import sys
sys.path.append('config/scripts/')

DeviceList = List[str]


class DeviceNotFoundException(Exception):
    pass


class Device(object):

    def __init__(self, name: str, script_name: str):

        self._running = True

        # Initialize midi library
        from pygame import midi
        self._midi = midi
        self._midi.init()

        if script_name.endswith('.py'):
            script_name = script_name[:-3]
        if script_name.endswith('.pyc'):
            script_name = script_name[:-4]

        self._module = import_module(script_name)
        self._settings = import_module('settings')

        # Iterate over all midi devices
        self._input_id = None
        self._output_id = None
        for x in range(0, self._midi.get_count()):
            # Check for name and if output or input
            if self._midi.get_device_info(x)[1].decode('ascii') == name and self._midi.get_device_info(x)[2] == 1:
                self._input_id = x
                self._input_device = self._midi.Input(x)
                self._settings.input_device = self._input_device
            if self._midi.get_device_info(x)[1].decode('ascii') == name and self._midi.get_device_info(x)[3] == 1:
                self._output_id = x
                self._output_device = self._midi.Output(x)
                self._settings.output_device = self._output_device

        if not self._output_id or not self._input_id:
            raise DeviceNotFoundException('No midi device with the name %s found.' % (name,))

    def close(self):
        self._running = False
        sleep(0.02)
        self._input_device.close()
        self._output_device.close()
        self._midi.quit()

    def read(self):
        while self._running:
            if self._input_device.poll():
                events = self._input_device.read(100)
                for event in events:
                    # process = Process(target=self._module.execute, args=(self.quit, self._output_device, event[0][0], event[0][1], event[0][2], event[0][3]))
                    # process.daemon = True
                    # process.start()

                    self._module.execute(self.close, self._settings, event[0][0], event[0][1], event[0][2], event[0][3])
            sleep(0.01)

    @staticmethod
    def get_devices() -> DeviceList:
        from pygame import midi
        midi.init()
        names = [midi.get_device_info(x)[1].decode('ascii') for x in range(0, midi.get_count())]
        midi.quit()
        return names
