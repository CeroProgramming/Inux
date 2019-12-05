from evdev import InputDevice, categorize, ecodes, list_devices
from asyncio import ensure_future, get_event_loop
from configparser import ConfigParser
from exec import execute


async def print_events(device):
    async for event in device.async_read_loop():
        print(device.path, categorize(event), sep=': ')



config = ConfigParser()
config.read('config/config.ini')

keyboards = config['DEFAULT']['keyboards'].split(',')
devices = list()

for keyboard in keyboards:
    id, code = execute("xinput --list --id-only '%s'" % (keyboard,))
    if code != 0:
        print("Keyboard with name '%s' not found. Skipping.." , (keyboard,))
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
