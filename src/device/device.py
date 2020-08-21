from evdev import InputDevice, list_devices

from logging import Logger
from importlib import import_module

from libs.exec import execute

# Get the id of the master device to reattach later
MASTER_DEVICE, CODE = execute('xinput list | grep "master device" | awk -F "master device" \'{print $2}\' |\
 cut -d"(" -f2 | cut -d")" -f1')  # FIXME Wrong id   TODO Support for multiple master devices
if CODE != 0:
    print("Couldn't get the id of the master device, So you need to reattach later by yourself. Find the master" +
          "device with 'xinput list' and execute 'xinput --reattach <your-device-id> <master-device-id>")
    MASTER_DEVICE = None
del CODE


class DeviceNotFoundException(Exception):
    pass


class Device(object):

    def __init__(self, name, logger: Logger, script_path: str):

        self._name = name
        self._is_created = False

        # Searching for the device
        self._id, self._initialization_code = execute("xinput --list --id-only '%s'" % (name,))
        self._id = self._id.strip()

        # Check if device was found
        if self._initialization_code != 0:
            print("Device with name '%s' and id %s not found. Skipping.." % (self._name, self._id))
            return

        # Disable device input
        _, self._disabling_code = execute("xinput float %s" % (self._id,))

        # Check if device was disabled
        if self._disabling_code != 0:
            print("Device with name '%s' and id %s could not be disabled. Skipping.." % (self._name, self._id))
            return

        self._device = None

        # Find the right device from /dev/input
        for device in [InputDevice(path) for path in list_devices()]:
            if device.name == self._name:
                print("Device with name '%s' and id %s found. Capturing.." % (self._name, self._id))
                self._device = device
            else:
                # Delete unused devices
                device.close()
                del device

        if not self._device:
            print("Device with name '%s' and id %s is not recognised. Skipping.." % (self._name, self._id))
            return

        self._script_path = script_path.replace('/', '.').replace('.py', '')
        self._script = import_module(self._script_path)

        self._logger = logger
        self._script.set_logger(logger)

        self._is_created = True

    def get_name(self) -> str:
        return self._name

    def get_id(self) -> int:
        return self._id

    def is_created(self) -> bool:
        return self._is_created

    def close(self) -> None:

        # Close input device
        self._device.close()

        # Reattach device to master if possible
        global MASTER_DEVICE
        if MASTER_DEVICE:
            execute("xinput --reattach %s %s" % (self._id, MASTER_DEVICE))

    def input_event(self, code: int, value: int):
        self._script.input_event(code, value)

    def async_read_loop(self):
        return self._device.async_read_loop()
