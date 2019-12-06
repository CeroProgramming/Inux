class MIDIController(object):

    def __init__(self):

        from pygame import midi

        self.initialized = False
        self.midi = midi

    def init(self):

        # Initialize midi library
        self.midi.init()
        self.initialized = True

    def quit(self):

        self.midi.quit()

    def get_device_id_by_name(self, name: str, output: bool = True) -> int:

        # Check if midi library is initialized
        if not self.initialized:
            self.init()
        # Iterate over all midi devices
        for x in range(0, self.midi.get_count()):
            # Check for name and if output or input
            if self.midi.get_device_info(x)[1].decode('ascii') == name and \
              self.midi.get_device_info(x)[2 if output else 3] == 1:
                return x
        # Return -1 if nothing was found
        return -1

    async def read(self, device_id: int):

        device = self.midi.Input(device_id)
        device.read(100)
