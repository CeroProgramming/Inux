#!/usr/bin/python3

from evdev import InputDevice, categorize, ecodes, list_devices
from asyncio import ensure_future, get_event_loop
from configparser import ConfigParser
from exec import execute
from argparse import ArgumentParser
from os.path import isfile

from keyboard import keypress, typing

class NoValidConfig(Exception):
    pass

parser = ArgumentParser(description='Linux Multiple Keyboard Input Controller')
parser.add_argument('--config', type=str, help='Pass the config file. Required!')

args = parser.parse_args()
configfp = vars(args)['config']

if not configfp:
    raise NoValidConfig('No config passed. Use flag --config <fp>.')
if not isfile(configfp):
    raise NoValidConfig('Passed file "%s" not found..' % (configfp,))

config = ConfigParser()
config.read(configfp)

async def print_events(device):
    async for event in device.async_read_loop():
        #print(device.path, categorize(event), sep=': ')
        if event.code == 0 or event.code == 4:
            continue
        print(f'code: {event.code} \nvalue:{event.value}')
        if event.code == 36 and event.value == 1:
            typing('Hello World')
        if event.code == 37:
            keypress('â', event.value)

keyboards = config['DEFAULT']['keyboards'].split(',')
devices = list()

for keyboard in keyboards:
    id, code = execute("xinput --list --id-only '%s'" % (keyboard,))
    if code != 0:
        print("Keyboard with name '%s' not found. Skipping.." % (keyboard,))
        continue
    execute("xinput float %s" % (id,))

    for element in [InputDevice(path) for path in list_devices()]:
        if element.name == keyboard:
            print("Keyboard with name '%s' found. Capturing.." % (keyboard,))
            devices.append(element)
        else:
            element.close()
            del element

for device in devices:
    ensure_future(print_events(device))

loop = get_event_loop()
loop.run_forever()
