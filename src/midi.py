from pygame import midi

INITIALIZED = False

def init():
    # Initialize midi library
    midi.init()
    INITIALIZED = True

def quit():
    midi.quit()

def get_device_id_by_name(name: str, output: bool = True) -> int:
    # Check if midi library is initalized
    if not INITIALIZED:
        init()
    # Iterate over all midi devices
    for x in range(0, midi.get_count()):
        # Check for name and if output or input
        if midi.get_device_info(x)[1].decode('ascii') == name and \
            midi.get_device_info(x)[2 if output else 3] == 1:
                return x
    # Return -1 if nothing was found
    return -1

async def read(id : int):
    device = midi.Input(id)
    device.read(100)
