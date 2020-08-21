from logging import Logger

# Some library examples for later use
from src.libs.keyboard import typing, type_special_character

# Map your keys here to a string so you don't have to remember the number for every key. To find out every number for
# every key, execute the program and checkout the 'code' attribute after pressing the key. If you are techie enough,
# feel free to provide a script that automates this part ;)
KCM = KEYCODE_MAPPING = {
    1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '', 9: '', 10: '', 11: '', 12: '',
    13: '', 14: '', 15: '', 16: '', 17: '', 18: '', 19: '', 20: '', 21: '', 22: '', 23: '', 24: '',
    25: '', 26: '', 27: '', 28: '', 29: '', 30: '', 31: '', 32: '', 33: '', 34: '', 35: '', 36: '',
    37: '', 38: '', 39: '', 40: '', 41: '', 42: '', 43: '', 44: '', 45: '', 46: '', 47: '', 48: '',
    49: '', 50: '', 51: '', 52: '', 53: '', 54: '', 55: '', 56: '', 57: '', 58: '', 59: '', 60: '',
    61: '', 62: '', 63: '', 64: '', 65: '', 66: '', 67: '', 68: '', 69: '', 70: '', 71: '', 72: '',
    73: '', 74: '', 75: '', 76: '', 77: '', 78: '', 79: '', 80: '', 81: '', 82: '', 83: '', 84: '',
    85: '', 86: '', 87: '', 88: '', 89: '', 90: '', 91: '', 92: '', 93: '', 94: '', 95: '', 96: '',
    97: '', 98: '', 99: '', 100: '', 101: '', 102: '', 103: '', 104: '', 105: '', 106: '', 107: '', 108: '',
    109: '', 110: '', 111: '', 112: '', 113: '', 114: '', 115: '', 116: '', 117: '', 118: '', 119: '', 120: '',
    121: '', 122: '', 123: '', 124: '', 125: '', 126: '', 127: ''
}

# Inverse the mapping, so you can access the keycodes by their name without writing everything again :)
KVM = KEY_VALUE_MAPPING = {v: k for k, v in KEYCODE_MAPPING.items()}

# This is to make a bit mapping were every control key is mapped to a single bit. I assume you to use the same names in
# the keycode mapping or to adjust the names here if you want to use it
CM = CONTROL_MAPPING = {
    KVM['CTRL_L']: 1,
    KVM['CTRL_R']: 2,
    KVM['ALT']: 4,
    KVM['ALT_GR']: 8,
    KVM['SUPER_L']: 16,
    KVM['SUPER_R']: 32,
    KVM['SHIFT_L']: 64,
    KVM['SHIFT_R']: 128,
    KVM['CAPSLOCK']: 256
}


# The Keyboard state holds the value of the control keys. You can also perform bitwise operations on the whole state
# instead of accessing the internal values
class KeyboardState:

    def __init__(self):
        self._mode = 0

    def __and__(self, other):
        self._mode &= other
        return self

    def __or__(self, other):
        self._mode |= other
        return self

    def __xor__(self, other):
        self._mode ^= other
        return self

    def __invert__(self):
        self._mode = ~self._mode
        return self

    def __int__(self):
        return self._mode

    def is_shift(self):
        return self._mode & (CM[KVM['SHIFT_L']] | CM[KVM['SHIFT_R']] | CM[KVM['CAPSLOCK']]) > 0

    def is_control(self):
        return self._mode & (CM[KVM['CTRL_L']] | CM[KVM['CTRL_R']]) > 0

    def is_alt(self):
        return self._mode & (CM[KVM['ALT']] | CM[KVM['ALT_GR']]) > 0

    def is_super(self):
        return self._mode & (CM[KVM['SUPER_L']] | CM[KVM['SUPER_R']]) > 0


class Keyboard:

    def __init__(self, logger: Logger):
        self.logger: Logger = logger
        self.state: KeyboardState = KeyboardState()
        self.layer: int = 0

    def input_event(self, code: int, value: int):

        if code in CM.keys() and value == 1:
            self.state |= CM[code]  # Set a bit value (if not already set)
        elif code in CM.keys() and value == 0:
            self.state ^= CM[code]  # Unset a bit value (if not already unset)
        elif KVM['F1'] <= code <= KVM['F10'] and value > 0:
            # This example contains a multi-layer keyboard. Every FN key maps to a other layer, so you can quickly
            # change the layout of your keyboard. Once again, the names for the key are just a suggestion like the
            # system at all.
            self.layer = code - KVM['F1']
        elif KVM['F11'] <= code <= KVM['F12'] and value > 0:
            # At least for me, F11 and F12 haven't the next values after the value of F10
            self.layer = code - KVM['F11'] + 10
        else:
            # Execute the function that belongs to the active layer
            eval('self.layer{}({}, {})'.format(self.layer, code, value))

        # Some logging stuff, so you can actually see whats going on
        self.logger.debug(f'code: {code} - mapping: {KCM[code]} - value: {value} - mode: {bin(int(self.state))}')

    def layer0(self, code: int, value: int):
        # An example on how to make the keys functional
        if code == KVM['K'] and value == 1:
            # See how I said 'equals 1' because I do not want to write the text multiple times if the key is pressed
            # longer. The value 1 typically means it just got pressed right now.
            typing('Hello World')
        elif code == KVM['L'] and value > 0:
            # Here I basically said 'after the key is pressed as long as it is not released'. 0 typically means the key
            # got released.
            type_special_character('😀')
        elif code == KVM['L'] and value > 0:
            # Instead of copy pasting emojis or other unicode characters, you can simply use their official name
            type_special_character("\N{CAT FACE}")

    def layer1(self, code: int, value: int):
        pass

    def layer2(self, code: int, value: int):
        pass

    def layer3(self, code: int, value: int):
        pass

    def layer4(self, code: int, value: int):
        pass

    def layer5(self, code: int, value: int):
        pass

    def layer6(self, code: int, value: int):
        pass

    def layer7(self, code: int, value: int):
        pass

    def layer8(self, code: int, value: int):
        pass

    def layer9(self, code: int, value: int):
        pass

    def layer10(self, code: int, value: int):
        pass

    def layer11(self, code: int, value: int):
        pass

    def layer12(self, code: int, value: int):
        pass


KEYBOARD: Keyboard


# This method gets called by the framework right after the keyboard is internally initialized
def set_logger(logger: Logger):
    global KEYBOARD
    KEYBOARD = Keyboard(logger)


# This method gets called by the framework everytime the device sends an event. We just pass it on here
def input_event(code: int, value: int):
    global KEYBOARD
    KEYBOARD.input_event(code, value)