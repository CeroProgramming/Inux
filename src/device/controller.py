from device.device import Device, DeviceNotFoundException
from config import Config
from logging import Logger

from asyncio import ensure_future, get_event_loop, new_event_loop, set_event_loop


async def print_events(device: Device):
    async for event in device.async_read_loop():
        device.input_event(event.code, event.value)


class Controller(object):

    def __init__(self, config: Config, logger: Logger):
        self._config = config
        self._devices = list()

        self._logger = logger
        self._loop = None

    def run(self):
        print(self._config.devices)

        for name, script in self._config.devices:
            try:
                device = Device(name, self._logger, script)
                self._devices.append(device)
            except DeviceNotFoundException as e:
                print('An exception with a device device occurred: ')
                print(e)

            for device in self._devices:
                ensure_future(print_events(device))

            self._loop = get_event_loop()
            self._loop.run_forever()

    def stop(self):
        for device in self._devices:
            device.close()







