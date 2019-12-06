#!/usr/bin/python3

from asyncio import ensure_future, get_event_loop

from config import Config
from arguments import Arguments
from keyboard import Keyboard
from libs.typing import keypress, typing


args = Arguments()

config = Config(args.get_config_fp())


async def print_events(device):
    async for event in device.async_read_loop():
        # print(device.path, categorize(event), sep=': ')
        if event.code == 0 or event.code == 4:
            continue
        print(f'code: {event.code} \nvalue:{event.value}')
        if event.code == 36 and event.value == 1:
            typing('Hello World')
        if event.code == 37:
            keypress('â', event.value)

keyboards = list()

for name in config.get_keyboards():
    keyboard = Keyboard(name)
    if keyboard.is_created():
        keyboards.append(keyboard)

for keyboard in keyboards:
    ensure_future(print_events(keyboard))

loop = get_event_loop()
loop.run_forever()
