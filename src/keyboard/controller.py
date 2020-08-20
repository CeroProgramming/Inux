from keyboard.keyboard import Keyboard, KeyboardNotFoundException
from config import Config
from logging import Logger

from asyncio import ensure_future, get_event_loop


async def print_events(device: Keyboard):
    async for event in device.async_read_loop():
        device.input_event(event.code, event.value)


class Controller(object):

    def __init__(self, config: Config, logger: Logger):
        self._config = config
        self._keyboards = list()

        for name, script in config.keyboards:
            try:
                keyboard = Keyboard(name, logger, script)
                self._keyboards.append(keyboard)
            except KeyboardNotFoundException as e:
                print('An exception with a keyboard device occurred: ')
                print(e)

            for keyboard in self._keyboards:
                ensure_future(print_events(keyboard))

            loop = get_event_loop()
            loop.run_forever()






