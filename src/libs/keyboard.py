from pynput.keyboard import Key, Controller
from pyperclip import copy, paste

keyController = Controller()


def type_special_character(key):
    cache = paste()
    copy(key)
    press(Key.ctrl.value)
    typing('v')
    release(Key.ctrl.value)
    copy(cache)


def press(key):
    keyController.press(key)


def release(key):
    keyController.release(key)


def keypress(key, status):
    if status == 1:
        press(key)
    elif status == 0:
        release(key)
    elif status == 2:
        release(key)
        press(key)


def typing(string):
    keyController.type(string)
